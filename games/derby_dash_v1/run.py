"""Derby Dash SDK simulation runner."""
import os
from gamestate import GameState
from game_config import GameConfig
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs
from utils.rgs_verification import execute_all_tests

if __name__=="__main__":
    config=GameConfig()
    gamestate=GameState(config)
    num_sim_args={"base":1000,"bonus":1000}
    create_books(gamestate, config, num_sim_args, 500, 1, True, False)
    generate_configs(gamestate)
    # RGS verifier writes its stats summary via a repo-root-relative path.
    # The workflow launches this script from the game directory, so ensure
    # that destination exists before verification.
    os.makedirs(os.path.join("games", config.game_id, "library"), exist_ok=True)
    execute_all_tests(config)
