"""Derby Dash ways executables."""
from src.calculations.ways import Ways
from src.events.events import (
    win_info_event,
    set_win_event,
    set_total_event,
)
from src.calculations.board import Board


class GameExecutables(Board):
    def evaluate_ways_board(self):
        """Evaluate frozen v0.35 ways plus Trophy scatter payout."""
        self.win_data = Ways.get_ways_data(
            self.config,
            self.board,
            global_multiplier=self.global_multiplier,
        )

        # engine.js applies PAY_SCALE to raw ways pays, then applies the feature
        # multiplier to the entire free-spin raw win.
        factor = self.config.pay_scale
        if self.gametype == self.config.freegame_type:
            factor *= self.config.bonus_win_multiplier

        for win in self.win_data["wins"]:
            win["win"] *= factor
            win["meta"]["winWithoutMult"] *= factor

        # Trophy pays independently of ways. In v0.35, every count >= 5 uses
        # the 5+ award (109.902 raw), including 6..15 Trophy boards.
        trophy_positions = []
        for reel, column in enumerate(self.board):
            for row, symbol in enumerate(column):
                if symbol.name == "T":
                    trophy_positions.append({"reel": reel, "row": row})

        scatter_count = len(trophy_positions)
        if scatter_count >= 3:
            pay_key = 3 if scatter_count == 3 else 4 if scatter_count == 4 else 5
            raw_scatter = self.config.scatter_raw_pay[pay_key]
            scatter_win = raw_scatter * factor
            self.win_data["wins"].append(
                {
                    "symbol": "T",
                    "kind": scatter_count,
                    "win": scatter_win,
                    "positions": trophy_positions,
                    "meta": {
                        "ways": 1,
                        "globalMult": factor,
                        "winWithoutMult": raw_scatter * self.config.pay_scale,
                        "scatter": True,
                    },
                }
            )

        # Preserve full internal precision like the frozen JS engine. RGS payout
        # granularity is handled only when Book is serialized.
        self.win_data["totalWin"] = sum(w["win"] for w in self.win_data["wins"])

        Ways.record_ways_wins(self)
        self.win_manager.update_spinwin(self.win_data["totalWin"])

        # Current SDK Ways emitter references a legacy evaluate_wincap hook.
        if self.win_manager.spin_win > 0:
            win_info_event(self)
            set_win_event(self)
        set_total_event(self)
