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

- **Steps:** 16 done, 4 skipped, 57 to go (of 77)
- **Bins emptied by consolidation:** 2 of 27 (A6, B3)
- **Empty bins in the shop now:** 39 of 223

**Still to do, by group:**

- Tools: steps 21-23
- Screws & nails: steps 24-41
- Bolts, nuts & anchors: steps 42-67
- Electrical: steps 68-77

**Next up:**

- Step 21: B13 → G13: M4 hex nuts; M5 hex nuts; M6 hex nuts; M4x8 hex head combination sc...
- Step 22: B17 → B10: Blue painter's tape
- Step 23: H10 → B2: Magnet pieces (broken, ceramic/ferrite style)
- Step 24: C9 → C10: Hex washer head sheet metal screws (zinc); Flat head self-drilling ...
- Step 25: C12 → F6: Rubber toggle-style hollow wall anchors
- Step 26: C12 → P4: Carriage bolts (zinc/stainless)
- Step 27: C14 → P11: Concrete/masonry screws with blue coating
- Step 28: F1 → C10: Hex head sheet metal / self-tapping screws, zinc

**Skipped:**

- Step 2: A1 → A11. Skipped: ratchet and socket stay in A1, they differ from the flat wrenches in A11
- Step 3: A1 → B2. Skipped: stays in A1, it belongs with the driver bits
- Step 14: B4 → B2. Skipped: tossed the foam sponge
- Step 19: B5 → J3. Skipped: about 30 assorted screws (machine, wood and self-tapping, one bag of long screws) left out loose to sort individually later; not in any bin yet
<!-- progress:end -->
