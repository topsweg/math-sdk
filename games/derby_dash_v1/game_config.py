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
        # Frozen v0.35 Trophy raw pays; 5 means 5-or-more scatters.
        self.scatter_raw_pay={3:8.788,4:35.152,5:109.902}
        self.starting_free_spins=10
        self.retrigger_free_spins=5
        self.final_stretch=((25,.35),(35,.30),(50,.20),(75,.10),(115,.04),(265,.01))

        # SDK symbol registration. Exact ways payouts are evaluated in Derby Dash GameState.
        self.paytable={(3,"G"):0.5273,(4,"G"):1.3182,(5,"G"):3.7355,(3,"SIL"):0.4394,(4,"SIL"):1.0990,(5,"SIL"):2.8567,(3,"TH"):0.3515,(4,"TH"):0.8788,(5,"TH"):2.2849,(3,"RF"):0.3081,(4,"RF"):0.7475,(5,"RF"):1.8455,(3,"A"):0.1980,(4,"A"):0.4394,(5,"A"):1.0546,(3,"K"):0.1758,(4,"K"):0.3960,(5,"K"):0.8788,(3,"Q"):0.1535,(4,"Q"):0.3515,(5,"Q"):0.7909,(3,"J"):0.1323,(4,"J"):0.3081,(5,"J"):0.6596}
        self.special_symbols={"wild":["W"],"scatter":["T"]}
        self.freespin_triggers={
            self.basegame_type:{3:10,4:10,5:10},
            self.freegame_type:{3:5,4:5,5:5},
        }
        self.anticipation_triggers={self.basegame_type:2,self.freegame_type:2}

        # Weighted-board GameState does not consume SDK reel strips, but Distribution
        # requires reel_weights. Keep a sentinel id here for SDK contract compliance.
        base_condition={"reel_weights":{self.basegame_type:{"WEIGHTED":1}},"force_wincap":False,"force_freegame":False}
        feature_condition={"reel_weights":{self.basegame_type:{"WEIGHTED":1},self.freegame_type:{"WEIGHTED":1}},
                           "scatter_triggers":{3:1},"force_wincap":False,"force_freegame":True}
        self.bet_modes=[
            BetMode(name="base",cost=1.0,rtp=self.rtp,max_win=self.wincap,
                auto_close_disabled=False,is_feature=True,is_buybonus=False,
                distributions=[
                    Distribution(criteria="freegame",quota=0.0035714285714285713,conditions=feature_condition),
                    Distribution(criteria="basegame",quota=0.9964285714285714,conditions=base_condition),
                ]),
            BetMode(name="bonus",cost=self.bonus_buy_cost,rtp=self.rtp,max_win=self.wincap,
                auto_close_disabled=False,is_feature=False,is_buybonus=True,
                distributions=[Distribution(criteria="freegame",quota=1.0,conditions=feature_condition)]),
        ]

    def final_stretch_mean(self):
        return sum(mult*p for mult,p in self.final_stretch)
