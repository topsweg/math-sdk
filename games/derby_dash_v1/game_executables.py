"""Derby Dash ways executables."""
from src.calculations.ways import Ways
from src.events.events import reveal_event, win_info_event, set_win_event, set_total_event, update_freespin_event, fs_trigger_event, freespin_end_event, final_win_event
from src.calculations.board import Board

class GameExecutables(Board):
    def evaluate_ways_board(self):
        self.win_data=Ways.get_ways_data(self.config,self.board,global_multiplier=self.global_multiplier)
        # v0.35 scale and feature multiplier are preserved explicitly.
        factor=self.config.pay_scale
        if self.gametype==self.config.freegame_type:
            factor*=self.config.bonus_win_multiplier
        for win in self.win_data["wins"]:
            win["win"]=round(win["win"]*factor,2)
            win["meta"]["winWithoutMult"]=round(win["meta"]["winWithoutMult"]*factor,2)
        self.win_data["totalWin"]=round(sum(w["win"] for w in self.win_data["wins"]),2)
        Ways.record_ways_wins(self)
        self.win_manager.update_spinwin(self.win_data["totalWin"])
        Ways.emit_wayswin_events(self)
