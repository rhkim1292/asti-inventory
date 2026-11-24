"""Apply finished consolidation steps to the inventory.

Usage:
    python consolidate.py 1-12,15      # mark steps done and move their rows
    python consolidate.py --list        # show steps that are not done yet

For each step in consolidation-plan.csv this moves the listed items from the
From bin to the To bin in inventory-detail.csv (tagging Notes with "Moved from X"),
sets the To bin's summary Contents when the step has a "To Becomes" value, and marks
the step Done. A From bin left with no detail rows becomes "Empty" in inventory.csv
and its photo in bin-image/ is deleted.
"""
import csv, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.join(ROOT, "consolidation-plan.csv")
DETAIL = os.path.join(ROOT, "inventory-detail.csv")
SUMMARY = os.path.join(ROOT, "inventory.csv")
IMAGES = os.path.join(ROOT, "bin-image")


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


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    pcols, plan = read(PLAN)
    if sys.argv[1] == "--list":
        for p in plan:
            if p["Status"] != "Done":
                print(f'{p["Step"]:>3}  {p["From"]:>4} -> {p["To"]:<4} {p["What"][:90]}')
        return

    want = parse_steps(sys.argv[1])
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
    write(PLAN, pcols, plan)
    for msg in problems:
        print("WARNING:", msg)


if __name__ == "__main__":
    main()
