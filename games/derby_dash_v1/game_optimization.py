"""Optimization targets for Derby Dash publish lookup tables."""
from optimization_program.optimization_config import ConstructParameters, ConstructConditions, verify_optimization_input

class OptimizationSetup:
    def __init__(self, game_config):
        self.game_config=game_config
        self.game_config.opt_params={
            "base":{
                "conditions":{
                    "freegame":ConstructConditions(rtp=0.342,hr=280).return_dict(),
                    "basegame":ConstructConditions(rtp=0.618,av_win=1.0).return_dict(),
                },
                "scaling":{},
                "parameters":ConstructParameters(num_show=5000,num_per_fence=10000,min_m2m=4,max_m2m=8,pmb_rtp=1.0,sim_trials=5000,test_spins=[50,100,200],test_weights=[0.3,0.4,0.3],score_type="rtp").return_dict(),
            },
            "bonus":{
                "conditions":{"freegame":ConstructConditions(rtp=0.96,hr="x",av_win=96.0).return_dict()},
                "scaling":{},
                "parameters":ConstructParameters(num_show=5000,num_per_fence=10000,min_m2m=4,max_m2m=8,pmb_rtp=1.0,sim_trials=5000,test_spins=[10,20,50],test_weights=[0.6,0.2,0.2],score_type="rtp").return_dict(),
            },
        }
        verify_optimization_input(self.game_config,self.game_config.opt_params)
