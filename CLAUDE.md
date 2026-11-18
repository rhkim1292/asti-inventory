# ASTI Shop Inventory

Inventory of shop storage bins, built from photos of each bin.

## How this project works
- The user sends a photo of a bin plus its label (bin letter + number, e.g. "A1").
- Identify the contents and add rows to `inventory.csv`.
- Photos are often sent from the Claude mobile app; edits also happen here in Claude Code. Always `git pull` before editing and commit + push after each bin so both sides stay in sync.

## inventory.csv format
One row per item type per bin (long format — do NOT make one column per item).

Columns: `Bin Letter,Bin Number,Item,Category,Qty,Notes`

- **Bin Letter / Bin Number**: split the label, e.g. A1 → `A`, `1`.
- **Item**: specific, searchable name (include sizes/brands when visible).
- **Category**: reuse existing categories where possible: Driver Bits, Nut Drivers, Bit Holders & Adapters, Drill Bits, Hand Tools, Sockets, Accessories, Misc. Add new ones only when nothing fits.
- **Qty**: exact if countable; prefix `~` for estimates.
- **Notes**: sizes, brand, condition (e.g. rusty), or "Unidentified" when unsure.
- Keep rows grouped by bin, in bin order.
- If a bin is re-photographed, replace that bin's rows rather than appending duplicates.

## Conventions
- Flag guesses in Notes instead of inventing specifics.
- Commit messages: `Add bin A2`, `Update bin A1`, etc.
