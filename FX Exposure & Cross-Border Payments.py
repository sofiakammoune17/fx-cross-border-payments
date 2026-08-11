"""
FX Exposure & Cross-Border Payments - case study for Flow
Educational model using illustrative assumptions, not live market quotes.

Scenario:
A European company must pay USD 100,000 in 3 months.
Compare:
1) unhedged payment;
2) 100% FX forward;
3) FX option protection;
4) partial forward hedge.

EUR/USD convention: USD per EUR.
"""

import pandas as pd
import matplotlib.pyplot as plt

USD_NOTIONAL = 100_000
SPOT = 1.16
EUR_RATE = 0.020
USD_RATE = 0.040
T = 0.25
OPTION_STRIKE = 1.16
OPTION_PREMIUM_PCT = 0.015
HEDGE_RATIO = 0.50
SCENARIOS = [1.05, 1.10, 1.16, 1.22, 1.28]

forward = SPOT * (1 + USD_RATE*T) / (1 + EUR_RATE*T)
initial_eur = USD_NOTIONAL / SPOT
premium_eur = initial_eur * OPTION_PREMIUM_PCT

def unhedged_cost(spot_t):
    return USD_NOTIONAL / spot_t

def forward_cost():
    return USD_NOTIONAL / forward

def option_cost(spot_t):
    # Right to buy USD at the strike. Exercise if EUR weakens.
    protected_cost = USD_NOTIONAL / OPTION_STRIKE
    market_cost = USD_NOTIONAL / spot_t
    return min(protected_cost, market_cost) + premium_eur

def partial_forward_cost(spot_t, hedge_ratio=HEDGE_RATIO):
    return hedge_ratio*forward_cost() + (1-hedge_ratio)*unhedged_cost(spot_t)

records = []
for s in SCENARIOS:
    u = unhedged_cost(s)
    f = forward_cost()
    o = option_cost(s)
    p = partial_forward_cost(s)
    records.append({
        "EURUSD_at_payment": s,
        "Unhedged_EUR": u,
        "Forward_EUR": f,
        "Option_EUR": o,
        "Partial_Forward_EUR": p,
        "Forward_saving_vs_unhedged": u-f,
        "Option_saving_vs_unhedged": u-o,
        "Partial_saving_vs_unhedged": u-p,
    })

df = pd.DataFrame(records)

print("FLOW FX CASE STUDY")
print(f"Theoretical 3M forward: {forward:.4f} USD per EUR")
print(f"100% forward EUR budget: {forward_cost():,.2f}")
print(f"Option premium: {premium_eur:,.2f} EUR")
print(df.round(2).to_string(index=False))

ax = df.plot(
    x="EURUSD_at_payment",
    y=["Unhedged_EUR", "Forward_EUR", "Option_EUR", "Partial_Forward_EUR"],
    marker="o",
    title="EUR cost of USD 100k payment across EUR/USD scenarios",
)
ax.set_xlabel("EUR/USD at payment date (USD per EUR)")
ax.set_ylabel("EUR payment cost")
plt.tight_layout()
plt.show()