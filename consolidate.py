"""Record consolidation progress.

Usage:
    python consolidate.py 1-12,15              # steps done: move their rows
    python consolidate.py --skip 11 "too full"  # steps skipped (nothing moves)
    python consolidate.py --list                # steps not done yet
    python consolidate.py --status              # just refresh the progress section

For each done step in consolidation-plan.csv this moves the listed items from the
From bin to the To bin in inventory-detail.csv (tagging Notes with "Moved from X"),
sets the To bin's summary Contents when the step has a "To Becomes" value, and marks
the step Done. A From bin left with no detail rows becomes "Empty" in inventory.csv
and its photo in bin-image/ is deleted. Every run rewrites the Progress section of
CONSOLIDATION.md.
"""
import csv, datetime, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.join(ROOT, "consolidation-plan.csv")
DETAIL = os.path.join(ROOT, "inventory-detail.csv")
SUMMARY = os.path.join(ROOT, "inventory.csv")
IMAGES = os.path.join(ROOT, "bin-image")
DOC = os.path.join(ROOT, "CONSOLIDATION.md")
START, END = "<!-- progress:start -->", "<!-- progress:end -->"


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


def write(path, cols, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def split(label):
    m = re.fullmatch(r"([A-Z]+)(\d+)", label.strip().upper())
    if not m:
        sys.exit(f"Bad bin label: {label}")
    return m.group(1), m.group(2)


def bin_key(letter, number):
    return (letter, int(number))


def parse_steps(spec):
    steps = set()
    for part in spec.split(","):
        a, _, b = part.partition("-")
        steps.update(range(int(a), int(b or a) + 1))
    return steps


def apply_done(plan, want):
    dcols, detail = read(DETAIL)
    scols, summary = read(SUMMARY)
    touched_from, problems = set(), []
    for p in plan:
        if int(p["Step"]) not in want:
            continue
        if p["Status"] == "Done":
            print(f'Step {p["Step"]} already done, skipping')
            continue
        fl, fn = split(p["From"])
        tl, tn = split(p["To"])
        items = [s.strip() for s in p["What"].split(" | ")]
        moved = 0
        for r in detail:
            if r["Bin Letter"] == fl and r["Bin Number"] == fn and r["Item"] in items:
                r["Bin Letter"], r["Bin Number"] = tl, tn
                tag = f'Moved from {p["From"]}'
                r["Notes"] = f'{r["Notes"]}; {tag}' if r["Notes"] else tag
                moved += 1
        if moved == 0:
            problems.append(f'Step {p["Step"]}: none of its items are in {p["From"]} any more')
            continue
        touched_from.add((fl, fn))
        if p["To Becomes"]:
            for s in summary:
                if s["Bin Letter"] == tl and s["Bin Number"] == tn:
                    s["Contents"] = p["To Becomes"]
        p["Status"] = "Done"
        print(f'Step {p["Step"]}: moved {moved} row(s) {p["From"]} -> {p["To"]}')

    # Keep detail rows grouped by bin, in bin order (stable within a bin).
    detail.sort(key=lambda r: bin_key(r["Bin Letter"], r["Bin Number"]))
    occupied = {(r["Bin Letter"], r["Bin Number"]) for r in detail}
    for fl, fn in sorted(touched_from):
        if (fl, fn) in occupied:
            continue
        for s in summary:
            if s["Bin Letter"] == fl and s["Bin Number"] == fn:
                s["Contents"] = "Empty"
        for ext in (".jpeg", ".jpg", ".png"):
            img = os.path.join(IMAGES, f"{fl}{fn}{ext}")
            if os.path.exists(img):
                os.remove(img)
        print(f"{fl}{fn} is now empty (summary set to Empty, photo removed)")

    write(DETAIL, dcols, detail)
    write(SUMMARY, scols, summary)
    for msg in problems:
        print("WARNING:", msg)


def apply_skip(plan, want, reason):
    for p in plan:
        if int(p["Step"]) in want and p["Status"] != "Done":
            p["Status"] = "Skipped"
            if reason:
                p["Note"] = f'{p["Note"]}; Skipped: {reason}' if p["Note"] else f"Skipped: {reason}"
            print(f'Step {p["Step"]} skipped')


def refresh_progress(plan):
    _, summary = read(SUMMARY)
    done = [p for p in plan if p["Status"] == "Done"]
    skipped = [p for p in plan if p["Status"] == "Skipped"]
    todo = [p for p in plan if p["Status"] not in ("Done", "Skipped")]
    emptied = [p["From"] for p in done if p["Empties From"] == "Yes"]
    empty_now = sum(1 for s in summary if s["Contents"] == "Empty")

    lines = [f"_Last updated {datetime.date.today().isoformat()} by consolidate.py. Do not edit this section by hand._", ""]
    lines.append(f"- **Steps:** {len(done)} done, {len(skipped)} skipped, {len(todo)} to go (of {len(plan)})")
    lines.append(f"- **Bins emptied by consolidation:** {len(emptied)} of "
                 f"{sum(1 for p in plan if p['Empties From'] == 'Yes')}"
                 + (f" ({', '.join(emptied)})" if emptied else ""))
    lines.append(f"- **Empty bins in the shop now:** {empty_now} of {len(summary)}")
    groups = []
    for p in todo:
        if p["Group"] not in groups:
            groups.append(p["Group"])
    if todo:
        lines += ["", "**Still to do, by group:**", ""]
        for g in groups:
            steps = [p for p in todo if p["Group"] == g]
            lines.append(f"- {g}: steps {compress([int(p['Step']) for p in steps])}")
        lines += ["", "**Next up:**", ""]
        for p in todo[:8]:
            what = p["What"].replace(" | ", "; ")
            what = what if len(what) <= 70 else what[:67] + "..."
            fit = " (check fit)" if "check fit" in p["Note"] else ""
            lines.append(f"- Step {p['Step']}: {p['From']} → {p['To']}: {what}{fit}")
    else:
        lines += ["", "**All steps are finished.**"]
    if skipped:
        lines += ["", "**Skipped:**", ""]
        for p in skipped:
            lines.append(f"- Step {p['Step']}: {p['From']} → {p['To']}. {p['Note']}")

    with open(DOC, encoding="utf-8") as f:
        doc = f.read()
    a, b = doc.index(START) + len(START), doc.index(END)
    doc = doc[:a] + "\n" + "\n".join(lines) + "\n" + doc[b:]
    with open(DOC, "w", encoding="utf-8", newline="\n") as f:
        f.write(doc)


def compress(nums):
    out, start = [], None
    for i, n in enumerate(nums):
        if start is None:
            start = n
        if i + 1 == len(nums) or nums[i + 1] != n + 1:
            out.append(str(start) if start == n else f"{start}-{n}")
            start = None
    return ", ".join(out)


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    pcols, plan = read(PLAN)
    if args[0] == "--list":
        for p in plan:
            if p["Status"] not in ("Done", "Skipped"):
                print(f'{p["Step"]:>3}  {p["From"]:>4} -> {p["To"]:<4} {p["What"][:90]}')
        return
    if args[0] == "--skip":
        if len(args) < 2:
            sys.exit(__doc__)
        apply_skip(plan, parse_steps(args[1]), " ".join(args[2:]))
    elif args[0] != "--status":
        apply_done(plan, parse_steps(args[0]))
    write(PLAN, pcols, plan)
    refresh_progress(plan)


if __name__ == "__main__":
    main()
