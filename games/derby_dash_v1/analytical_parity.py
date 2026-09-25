"""Exact analytical parity checks for frozen Derby Dash v0.35 invariants."""
from math import comb, isclose
from game_config import GameConfig

C=GameConfig()
TOTAL=sum(C.base_weights.values())
P_T=C.base_weights["T"]/TOTAL

def binom_tail(n,k,p):
    return sum(comb(n,i)*p**i*(1-p)**(n-i) for i in range(k,n+1))

# Natural feature: >=3 trophies anywhere in the 15 IID cells.
feature_p=binom_tail(15,3,P_T)

# Reel-5 anticipation/tease: >=2 trophies in first four reels = first 12 IID cells.
tease_p=binom_tail(12,2,P_T)

# Final Stretch expectation.
final_mean=sum(mult*prob for mult,prob in C.final_stretch)

# Bonus retrigger probability uses the same Trophy weight as base.
retrigger_p=feature_p
expected_fs=C.starting_free_spins/(1-C.retrigger_free_spins*retrigger_p)

print("DERBY DASH v0.35 ANALYTICAL PARITY")
print(f"total_symbol_weight={TOTAL:.10f}")
print(f"trophy_cell_probability={P_T:.12%}")
print(f"natural_feature_probability={feature_p:.12%}")
print(f"natural_feature_odds=1 in {1/feature_p:.9f}")
print(f"reel5_tease_probability={tease_p:.12%}")
print(f"reel5_tease_odds=1 in {1/tease_p:.9f}")
print(f"final_stretch_mean={final_mean:.12f}x")
print(f"expected_free_spin_length={expected_fs:.12f}")

# Frozen design invariants / independently exact expectations.
assert isclose(feature_p,1/280,rel_tol=0,abs_tol=1e-12), feature_p
assert abs((1/tease_p)-38.9)<0.1, 1/tease_p
assert isclose(final_mean,44.0,rel_tol=0,abs_tol=1e-12), final_mean
assert C.starting_free_spins==10
assert C.retrigger_free_spins==5
assert C.free_weights["W"]==2*C.base_weights["W"]
assert isclose(C.bonus_buy_cost,100.0)
print("ANALYTICAL PARITY: PASS")
