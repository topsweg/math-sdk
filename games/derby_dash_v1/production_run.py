"""Generate publish-ready Derby Dash math.

Frozen candidate: Final Stretch mean 1.832x, 5000x cap, target RTP 96%.
"""
from gamestate import GameState
from game_config import GameConfig
from game_optimization import OptimizationSetup
from optimization_program.run_script import OptimizationExecution
from utils.rgs_verification import execute_all_tests
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__=="__main__":
    config=GameConfig(); gamestate=GameState(config); OptimizationSetup(config)
    sims={"base":100000,"bonus":100000}
    create_books(gamestate,config,sims,5000,10,True,False)
    generate_configs(gamestate)
    OptimizationExecution().run_all_modes(config,list(sims.keys()),10)
    generate_configs(gamestate)
    execute_all_tests(config)
