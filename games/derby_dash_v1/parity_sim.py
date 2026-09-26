"""Large Derby Dash parity simulation for Final Stretch purse-multiplier math, independent of SDK forcing."""
import random
from game_config import GameConfig
C=GameConfig(); SYMS=list(C.base_weights); PAY=C.paytable
def pick(w): return random.choices(SYMS,weights=[w[s] for s in SYMS],k=1)[0]
def grid(w): return [[pick(w) for _ in range(3)] for _ in range(5)]
def evaluate(g,bonus=False):
    total=0.0
    for s in ("G","SIL","TH","RF","A","K","Q","J"):
        counts=[]
        for reel in g:
            n=sum(x==s or x=="W" for x in reel)
            if not n: break
            counts.append(n)
        if len(counts)>=3:
            ways=1
            for n in counts: ways*=n
            total+=PAY[(len(counts),s)]*C.pay_scale*ways
    scat=sum(x=="T" for reel in g for x in reel)
    if scat>=3:
        key=3 if scat==3 else 4 if scat==4 else 5
        total+=C.scatter_raw_pay[key]*C.pay_scale
    return total*(C.bonus_win_multiplier if bonus else 1),scat
def finish():
    return random.choices([x[0] for x in C.final_stretch],weights=[x[1] for x in C.final_stretch],k=1)[0]
def bonus():
    left=C.starting_free_spins; played=retr=0; win=0.0
    while left:
        left-=1; played+=1
        w,sc=evaluate(grid(C.free_weights),True); win+=w
        if sc>=3: left+=C.retrigger_free_spins; retr+=1
    return win*finish(),played,retr
def main(base_n=3_000_000,buy_n=300_000,seed=350035):
    random.seed(seed); paid=base=feature=0.0; triggers=hits=teases=0; feature_spins=feature_retr=0
    max_paid=0.0; max_feature=0.0
    for _ in range(base_n):
        g=grid(C.base_weights); w,sc=evaluate(g); base+=w; hits+=w>0
        teases+=sum(x=="T" for reel in g[:4] for x in reel)>=2
        bw=0.0
        if sc>=3:
            triggers+=1; bw,sp,rt=bonus(); feature+=bw; feature_spins+=sp; feature_retr+=rt
        round_win=w+bw; paid+=round_win; max_paid=max(max_paid,round_win); max_feature=max(max_feature,bw)
    buy=0.0; buy_spins=buy_retr=0; max_buy=0.0
    for _ in range(buy_n):
        w,sp,rt=bonus(); buy+=w; max_buy=max(max_buy,w); buy_spins+=sp; buy_retr+=rt
    print("DERBY DASH FINAL STRETCH v2 PARITY")
    print(f"paid_rounds={base_n:,} bonus_buys={buy_n:,}")
    print(f"paid_rtp={paid/base_n:.6%}"); print(f"base_rtp={base/base_n:.6%}")
    print(f"natural_feature_rtp={feature/base_n:.6%}"); print(f"hit_rate={hits/base_n:.6%}")
    print(f"natural_feature_rate={triggers/base_n:.6%} (1 in {base_n/triggers:.2f})")
    print(f"reel5_tease={teases/base_n:.6%} (1 in {base_n/teases:.2f})")
    print(f"avg_natural_feature={feature/triggers:.6f}x")
    print(f"avg_natural_fs_length={feature_spins/triggers:.6f}")
    print(f"retriggers_per_natural={feature_retr/triggers:.6f}")
    print(f"bonus_buy_rtp={buy/(buy_n*C.bonus_buy_cost):.6%}")
    print(f"avg_bonus_buy={buy/buy_n:.6f}x"); print(f"avg_buy_fs_length={buy_spins/buy_n:.6f}")
    print(f"retriggers_per_buy={buy_retr/buy_n:.6f}")
    print(f"final_stretch_mean={C.final_stretch_mean():.6f}x")
    print(f"max_paid_round={max_paid:.6f}x"); print(f"max_natural_feature={max_feature:.6f}x")
    print(f"max_bonus_buy={max_buy:.6f}x")
if __name__=="__main__": main()
