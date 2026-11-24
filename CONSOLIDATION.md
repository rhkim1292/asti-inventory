# Shop Inventory Consolidation

Goal: free up bins by combining bins that hold the same kind of thing, and by sending stray items to the bin where their kind lives. The step-by-step moves are in [consolidation-plan.csv](consolidation-plan.csv).

## Decisions already made (don't re-ask)
- **Merge in place first.** Use the bins where things already are. Regrouping the shelves into zones (e.g. all bolts in one row) is a possible later round, not part of this plan.
- **All bins are about the same size**, so any bin can take any other bin's contents if there's room.
- **Keep everything.** Nothing gets thrown out unless the user says they tossed something.
- **Bag moved parts** when the target bin already has loose parts, so different screws don't mix.
- How full each bin is ("To Fill (est.)" in the plan) was estimated from the bin photos on 2026-11-24. If the user says something doesn't fit, believe them over the estimate.

## How the plan works
- 77 steps in 4 groups: Tools, Screws & nails, Bolts/nuts/anchors, Electrical. Within a group, steps are sorted by the bin things come **out of**, so the user can open one bin and hand everything out from it.
- Each step lists the From bin, the To bin, the exact items, whether it empties the From bin, and what the To bin should be called afterwards ("To Becomes").
- Doing every step empties 28 more bins, taking the shop from 37 empty bins to 65.
- Steps 11, 56, 57 and 58 say **check fit**: the target may be too tight. If it is, the step gets skipped.
- B2 becomes the **misc & oddballs** bin for things that don't belong anywhere else.

## Recording progress (for Claude, including from the phone)
Always `git pull` first, then commit and push after each update.

| User says | Run |
|---|---|
| "done 1-12" / "finished steps 1 to 12" | `python consolidate.py 1-12` |
| "skip 11, didn't fit" | `python consolidate.py --skip 11 "didn't fit"` |
| "what's next?" | read the Progress section below (or `python consolidate.py --list`) |
| "put step 56 in K11 instead" | edit that row's `To` (and `To Becomes` if needed) in the plan with the csv module, then run the step when it's done |
| "I tossed the rusty nails in F2" | update the detail rows the normal way (see CLAUDE.md) |

- `consolidate.py` moves the rows in both spreadsheets, sets emptied bins to `Empty`, deletes their photos, renames target bins, marks steps Done or Skipped, and rewrites the Progress section below. Never edit those things by hand.
- Commit message: `Consolidate steps 1-12` (or `Skip consolidation step 11`).
- When the user re-photographs a bin that received items, update it the normal way (replace its rows). The photo wins over the moved rows.

## Progress
<!-- progress:start -->
_Last updated 2026-11-24 by consolidate.py. Do not edit this section by hand._

- **Steps:** 0 done, 0 skipped, 77 to go (of 77)
- **Bins emptied by consolidation:** 0 of 28
- **Empty bins in the shop now:** 37 of 223

**Still to do, by group:**

- Tools: steps 1-23
- Screws & nails: steps 24-41
- Bolts, nuts & anchors: steps 42-67
- Electrical: steps 68-77

**Next up:**

- Step 1: A1 → A5: Forstner bits (long shank)
- Step 2: A1 → A11: Craftsman 1/4" ratchet; Socket (Craftsman chrome)
- Step 3: A1 → B2: Black rubber block/pad; Bag of small metal parts
- Step 4: A5 → A3: End mill / spiral router bit
- Step 5: A5 → A11: Thin open-end tool wrenches
- Step 6: A6 → A5: Spade bits (1/4" hex shank, extended length)
- Step 7: B2 → A1: Hex-shank socket adapter
- Step 8: B2 → B4: Allen key (L-shaped)
<!-- progress:end -->
