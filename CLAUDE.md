# ASTI Shop Inventory

Inventory of shop storage bins, built from photos of each bin.

## How this project works
- The user sends a photo of a bin plus its label (bin letter + number, e.g. "A1").
- Identify the contents and update BOTH spreadsheets: `inventory.csv` (summary) and `inventory-detail.csv` (detail).
- Save the bin's photo to `bin-image/` named after the bin label, e.g. `bin-image/A1.jpeg`. If a bin is re-photographed, overwrite its image.
- Photos are often sent from the Claude mobile app; edits also happen here in Claude Code. Always `git pull` before editing and commit + push after each bin so both sides stay in sync.

## inventory.csv (summary — one row per bin)
Columns: `Bin Letter,Bin Number,Contents`

- **Contents**: a general description/concept of the bin in 1–3 words (e.g. "Driver bits", "Taps & dies").

## inventory-detail.csv (detail — one row per item type per bin)
Long format — do NOT make one column per item.

Columns: `Bin Letter,Bin Number,Item,Category,Family,Qty,Notes`

- **Item**: specific, searchable name (include sizes/brands when visible).
- **Category**: reuse existing categories where possible: Driver Bits, Nut Drivers, Bit Holders & Adapters, Drill Bits, Hand Tools, Sockets, Knives, Blades, Router Bits, Router Accessories, Taps & Dies, Fasteners, Rotary Tool Accessories, Plastic Caps, Hose Clamps, Hardware, Abrasives, Writing & Marking, Painting, Adhesives, Documents, Welding, Safety, Plumbing, Electrical, Accessories, Misc. Add new ones only when nothing fits.
- **Family**: a narrower group than Category, used to find things that belong together (e.g. Wood screws, Drywall screws, Hex nuts, Washers, Wedge anchors → "Concrete anchors", EMT fittings → "Conduit fittings"). Reuse a value already in the file; add a new one only when nothing fits. For tool categories, Family usually equals Category.
- **Qty**: exact if countable; prefix `~` for estimates.
- **Notes**: sizes, brand, condition (e.g. rusty), or "Unidentified" when unsure.

## Rules for both files
- **Bin Letter / Bin Number**: split the label, e.g. A1 → `A`, `1`.
- Keep rows grouped by bin, in bin order.
- Empty bins: add a summary row with Contents `Empty` and no rows in the detail file.
- If a bin is re-photographed, replace that bin's rows rather than appending duplicates.
- Write the files with a real CSV library (e.g. Python's `csv` module), never by hand. Any field containing a comma or a `"` (like the inch mark in `1/4"`) must be wrapped in quotes with inner quotes doubled — otherwise GitHub can't render the file as a table.

## Consolidation (in progress)
- `consolidation-plan.csv` lists numbered moves (From bin → To bin, which items). The user does them in the shop and reports which steps are done (e.g. "done 1-12", or "skip 56, didn't fit").
- Record finished steps with `python consolidate.py 1-12` (never by hand). It moves the detail rows, tags Notes with "Moved from X", sets the To bin's Contents from "To Becomes", marks emptied bins `Empty`, deletes their photos and marks the steps Done. `python consolidate.py --list` shows what's left.
- If a step was skipped or changed, edit that row of the plan (Status `Skipped`, or a new To bin) instead of running it.
- After the user re-photographs a bin that received items, update it the normal way (replace its rows).
- Commit once per batch: `Consolidate steps 1-12`.

## Conventions
- Flag guesses in Notes instead of inventing specifics.
- Commit messages: `Add bin A2`, `Update bin A1`, etc.
