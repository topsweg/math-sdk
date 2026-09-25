"""Derby Dash SDK GameState."""
import random
from game_override import GameStateOverride
from src.events.events import fs_trigger_event, update_freespin_event, freespin_end_event, final_win_event
from src.state.books import Book

class DerbyBook(Book):
    """Derby-specific RGS serialization; leave the shared SDK Book contract untouched."""
    def to_json(self):
        data=super().to_json()
        data["payoutMultiplier"]=int(round(self.payout_multiplier*10,0)*10)
        return data

class GameState(GameStateOverride):
    def reset_book(self):
        """Use Derby's 0.1x RGS payout quantization only for Derby books."""
        super().reset_book()
        derby_book=DerbyBook(self.book.id,self.book.criteria)
        derby_book.events=self.book.events
        derby_book.payout_multiplier=self.book.payout_multiplier
        derby_book.basegame_wins=self.book.basegame_wins
        derby_book.freegame_wins=self.book.freegame_wins
        self.book=derby_book

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
        # Final Stretch is a separate feature award, not part of the last free-spin reveal.
        self.win_manager.reset_spin_win()
        mult=random.choices([x[0] for x in self.config.final_stretch],
                            weights=[x[1] for x in self.config.final_stretch],k=1)[0]
        runners=["Midnight Royale","Golden Gallop","Silver Comet"]
        winner_index=random.randrange(len(runners))
        winner=runners[winner_index]

        # Frozen v0.35 presentation contract: the winning runner shows the actual
        # award; the other two show distinct alternatives excluding that award.
        all_prizes=[x[0] for x in self.config.final_stretch]
        alternatives=[x for x in all_prizes if x != mult]
        other_prizes=random.sample(alternatives,2)
        prizes=[None]*len(runners)
        prizes[winner_index]=mult
        other_indexes=[i for i in range(len(runners)) if i != winner_index]
        prizes[other_indexes[0]]=other_prizes[0]
        prizes[other_indexes[1]]=other_prizes[1]

        self.final_stretch_multiplier=mult
        self.add_derby_event(
            "finalStretch",
            runners=runners,
            winner=winner,
            winnerIndex=winner_index,
            multiplier=mult,
            win=mult,
            prizes=prizes,
        )
        self.win_manager.update_spinwin(mult)
        self.win_manager.update_gametype_wins(self.gametype)

    def update_final_win(self):
        """Serialize rounded SDK book totals without rounding Derby's internal math."""
        final=round(min(self.win_manager.running_bet_win,self.config.wincap),2)
        base=round(min(self.win_manager.basegame_wins,self.config.wincap),2)
        # Rounding base/free independently can differ from rounded total by 0.01.
        # Reconcile the book split to the authoritative rounded round total.
        free=round(final-base,2)
        self.final_win=final
        self.book.payout_multiplier=final
        self.book.basegame_wins=base
        self.book.freegame_wins=free
        assert round(self.book.basegame_wins+self.book.freegame_wins,2)==final

    def run_spin(self,sim,simulation_seed=None):
        self.reset_seed(sim,simulation_seed)
        self.repeat=True
        while self.repeat:
            self.reset_book()

            # v0.35 Bonus Buy enters Winner's Circle directly: no base board,
            # no natural-trigger fishing, 10 starting free spins.
            if self.get_current_betmode().get_buybonus():
                self.tot_fs=self.config.starting_free_spins
                self.triggered_freegame=True
                self.gametype=self.config.freegame_type
                self.run_freespin()
            else:
                self.gametype=self.config.basegame_type
                self.draw_weighted_board(False)
                self.evaluate_ways_board()
                self.win_manager.update_gametype_wins(self.gametype)
                if self.check_trophy_trigger():
                    self.tot_fs=self.config.starting_free_spins
                    self.triggered_freegame=True
                    fs_trigger_event(
                        self,
                        include_padding_index=False,
                        basegame_trigger=True,
                        freegame_trigger=False,
                    )
                    self.gametype=self.config.freegame_type
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
