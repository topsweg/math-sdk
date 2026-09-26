"""Derby Dash state overrides."""
from game_executables import GameExecutables

class GameStateOverride(GameExecutables):
    def assign_special_sym_function(self):
        self.special_symbol_functions={}

    def reset_book(self):
        super().reset_book()
        self.final_stretch_multiplier=0

    def add_derby_event(self,event_type,**payload):
        self.book.add_event({"index":len(self.book.events),"type":event_type,**payload})

    def set_reel5_anticipation(self):
        # Approved frontend behavior: only reel 5 extends when first four reels contain 2+ Trophies.
        count=sum(1 for reel in self.board[:4] for sym in reel if sym.name=="T")
        self.anticipation=[0,0,0,0,1 if count>=2 else 0]
