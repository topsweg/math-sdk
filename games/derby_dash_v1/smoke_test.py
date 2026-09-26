"""Fast config/parity smoke test. Run from repository root."""
from game_config import GameConfig

if __name__=="__main__":
    c=GameConfig()
    assert c.game_id=="derby_dash_v1"
    assert c.num_reels==5 and c.num_rows==[3]*5
    assert c.free_weights["W"]==2*c.base_weights["W"]
    assert abs(c.final_stretch_mean()-1.843)<1e-12
    assert c.starting_free_spins==10 and c.retrigger_free_spins==5
    assert c.bonus_buy_cost==100.0
    print("Derby Dash SDK config smoke test: PASS")
    print(f"Final Stretch mean: {c.final_stretch_mean():.3f}x")
