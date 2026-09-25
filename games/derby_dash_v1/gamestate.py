"""Derby Dash SDK GameState."""
import random
from game_override import GameStateOverride
from src.events.events import fs_trigger_event, update_freespin_event, freespin_end_event, final_win_event

class GameState(GameStateOverride):
    def _weighted_symbol(self,weights):
        names=list(weights); vals=list(weights.values())
        return random.choices(names,weights=vals,k=1)[0]

    def draw_weighted_board(self,bonus=False):
        self.refresh_special_syms()
        weights=self.config.free_weights if bonus else self.config.base_weights
        self.board=[[self.create_symbol(self._weighted_symbol(weights)) for _ in range(3)] for _ in range(5)]
        self.get_special_symbols_on_board()
        self.reel_positions=[0]*5
        self.set_reel5_anticipation()
        # Native reveal shape, without reel padding.
        from src.events.events import reveal_event
        reveal_event(self)

    def check_trophy_trigger(self):
        return self.count_special_symbols("scatter")>=3

    def _final_stretch(self):
        mult=random.choices([x[0] for x in self.config.final_stretch],
                            weights=[x[1] for x in self.config.final_stretch],k=1)[0]
        runners=["Midnight Royale","Golden Gallop","Silver Comet"]
        winner=random.choice(runners)
        self.final_stretch_multiplier=mult
        self.add_derby_event("finalStretch",runners=runners,winner=winner,multiplier=mult,win=mult)
        self.win_manager.update_spinwin(mult)
        self.win_manager.update_gametype_wins(self.gametype)

    def run_spin(self,sim,simulation_seed=None):
        self.reset_seed(sim,simulation_seed)
        self.repeat=True
        while self.repeat:
            self.reset_book()
            self.gametype=self.config.basegame_type
            self.draw_weighted_board(False)
            self.evaluate_ways_board()
            self.win_manager.update_gametype_wins(self.gametype)
            if self.check_trophy_trigger():
                self.tot_fs=self.config.starting_free_spins
                self.triggered_freegame=True
                fs_trigger_event(self,include_padding_index=False,basegame_trigger=True,freegame_trigger=False)
                self.run_freespin()
            self.update_final_win()
            self.check_repeat()
        self.imprint_wins()

    def run_freespin(self):
        self.reset_fs_spin()
        # Bonus-buy criteria enters the feature directly.
        if self.tot_fs==0: self.tot_fs=self.config.starting_free_spins
        while self.fs<self.tot_fs:
            self.fs+=1
            self.win_manager.reset_spin_win()
            update_freespin_event(self)
            self.draw_weighted_board(True)
            self.evaluate_ways_board()
            if self.check_trophy_trigger():
                self.tot_fs+=self.config.retrigger_free_spins
                fs_trigger_event(self,include_padding_index=False,basegame_trigger=False,freegame_trigger=True)
            self.win_manager.update_gametype_wins(self.gametype)
        self._final_stretch()
        freespin_end_event(self)
