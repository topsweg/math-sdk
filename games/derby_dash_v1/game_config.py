"""Derby Dash SDK configuration — frozen v0.35 math target."""
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode

class GameConfig(Config):
    _instance=None
    def __new__(cls):
        if cls._instance is None: cls._instance=super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.game_id="derby_dash_v1"
        self.provider_number=0
        self.working_name="Derby Dash"
        self.win_type="ways"
        self.rtp=0.96
        self.wincap=5000.0
        self.construct_paths()
        self.num_reels=5
        self.num_rows=[3]*5
        self.include_padding=False

        self.base_weights={"W":3,"G":6,"SIL":8,"TH":10,"RF":12,"T":2.3585721393,"A":16,"K":17,"Q":18,"J":19}
        self.free_weights={**self.base_weights,"W":6}
        self.pay_scale=1.3595694474
        self.bonus_win_multiplier=5.0674552348
        self.bonus_buy_cost=100.0
        self.starting_free_spins=10
        self.retrigger_free_spins=5
        self.final_stretch=((25,.35),(35,.30),(50,.20),(75,.10),(115,.04),(265,.01))

        # SDK symbol registration. Exact ways payouts are evaluated in Derby Dash GameState.
        self.paytable={(3,s):0.0 for s in ("W","G","SIL","TH","RF","A","K","Q","J")}
        self.special_symbols={"wild":["W"],"scatter":["T"]}
        self.freespin_triggers={
            self.basegame_type:{3:10,4:10,5:10},
            self.freegame_type:{3:5,4:5,5:5},
        }
        self.anticipation_triggers={self.basegame_type:2,self.freegame_type:2}

        base_condition={"force_wincap":False,"force_freegame":False}
        feature_condition={"force_wincap":False,"force_freegame":True}
        self.bet_modes=[
            BetMode(name="base",cost=1.0,rtp=self.rtp,max_win=self.wincap,
                auto_close_disabled=False,is_feature=True,is_buybonus=False,
                distributions=[
                    Distribution(criteria="freegame",quota=0.01,conditions=feature_condition),
                    Distribution(criteria="basegame",quota=0.99,conditions=base_condition),
                ]),
            BetMode(name="bonus",cost=self.bonus_buy_cost,rtp=self.rtp,max_win=self.wincap,
                auto_close_disabled=False,is_feature=False,is_buybonus=True,
                distributions=[Distribution(criteria="freegame",quota=1.0,conditions=feature_condition)]),
        ]

    def final_stretch_mean(self):
        return sum(mult*p for mult,p in self.final_stretch)
