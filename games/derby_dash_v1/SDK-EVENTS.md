# Derby Dash SDK book events

The first native port emits the SDK's standard reveal/win/free-spin/final-win events plus one Derby-specific event:

- reveal
- winInfo / setWin / setTotalWin
- freeSpinTrigger
- updateFreeSpin
- freeSpinRetrigger
- finalStretch
- freeSpinEnd
- finalWin

The browser adapter should map these deterministic book events to the existing v0.35 presentation.
The race animation must never select or modify the winner; the book's finalStretch event is authoritative.
