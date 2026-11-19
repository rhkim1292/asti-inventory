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

Columns: `Bin Letter,Bin Number,Item,Category,Qty,Notes`

- **Item**: specific, searchable name (include sizes/brands when visible).
- **Category**: reuse existing categories where possible: Driver Bits, Nut Drivers, Bit Holders & Adapters, Drill Bits, Hand Tools, Sockets, Knives, Blades, Router Bits, Router Accessories, Taps & Dies, Fasteners, Accessories, Misc. Add new ones only when nothing fits.
- **Qty**: exact if countable; prefix `~` for estimates.
- **Notes**: sizes, brand, condition (e.g. rusty), or "Unidentified" when unsure.

## Rules for both files
- **Bin Letter / Bin Number**: split the label, e.g. A1 → `A`, `1`.
- Keep rows grouped by bin, in bin order.
- If a bin is re-photographed, replace that bin's rows rather than appending duplicates.
- Write the files with a real CSV library (e.g. Python's `csv` module), never by hand. Any field containing a comma or a `"` (like the inch mark in `1/4"`) must be wrapped in quotes with inner quotes doubled — otherwise GitHub can't render the file as a table.

## Conventions
- Flag guesses in Notes instead of inventing specifics.
- Commit messages: `Add bin A2`, `Update bin A1`, etc.
