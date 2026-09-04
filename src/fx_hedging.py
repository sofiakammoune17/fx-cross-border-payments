"""Corporate FX exposure and hedging scenario engine.

All rates and market inputs are illustrative and are not live quotations.
EUR/USD is expressed as USD per EUR.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


@dataclass(frozen=True)
class FXExposure:
    usd_notional: float = 100_000.0
    spot: float = 1.16
    eur_rate: float = 0.02
    usd_rate: float = 0.04
    maturity_years: float = 0.25
    option_strike: float = 1.16
    option_premium_pct: float = 0.015
    hedge_ratio: float = 0.50

    def __post_init__(self) -> None:
        if self.usd_notional <= 0 or self.spot <= 0 or self.option_strike <= 0:
            raise ValueError("Notional, spot and strike must be positive.")
        if self.maturity_years <= 0:
            raise ValueError("Maturity must be positive.")
        if not 0 <= self.hedge_ratio <= 1:
            raise ValueError("Hedge ratio must be between 0 and 1.")

    @property
    def forward_rate(self) -> float:
        """Deliverable forward rate from covered interest parity."""
        return self.spot * (1 + self.usd_rate * self.maturity_years) / (
            1 + self.eur_rate * self.maturity_years
        )

    @property
    def option_premium_eur(self) -> float:
        return self.usd_notional / self.spot * self.option_premium_pct

    def unhedged_cost(self, terminal_spot: float) -> float:
        return self.usd_notional / terminal_spot

    def forward_cost(self) -> float:
        return self.usd_notional / self.forward_rate

    def option_cost(self, terminal_spot: float) -> float:
        protected_cost = self.usd_notional / self.option_strike
        return min(protected_cost, self.unhedged_cost(terminal_spot)) + self.option_premium_eur

    def partial_forward_cost(self, terminal_spot: float) -> float:
        return self.hedge_ratio * self.forward_cost() + (
            1 - self.hedge_ratio
        ) * self.unhedged_cost(terminal_spot)


def build_scenario_table(exposure: FXExposure, scenarios: list[float]) -> pd.DataFrame:
    if not scenarios or any(spot <= 0 for spot in scenarios):
        raise ValueError("Scenarios must contain positive EUR/USD rates.")

    records = []
    for terminal_spot in scenarios:
        unhedged = exposure.unhedged_cost(terminal_spot)
        forward = exposure.forward_cost()
        option = exposure.option_cost(terminal_spot)
        partial = exposure.partial_forward_cost(terminal_spot)
        costs = {
            "Unhedged": unhedged,
            "Forward": forward,
            "Option": option,
            "Partial forward": partial,
        }
        records.append(
            {
                "EURUSD_at_payment": terminal_spot,
                **{f"{name}_EUR": value for name, value in costs.items()},
                "Lowest_cost_strategy": min(costs, key=costs.get),
                "Forward_vs_unhedged_EUR": forward - unhedged,
                "Option_vs_unhedged_EUR": option - unhedged,
                "Partial_vs_unhedged_EUR": partial - unhedged,
            }
        )
    return pd.DataFrame(records)


def save_outputs(table: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    table.to_csv(output_dir / "fx_hedging_scenarios.csv", index=False)

    ax = table.plot(
        x="EURUSD_at_payment",
        y=["Unhedged_EUR", "Forward_EUR", "Option_EUR", "Partial forward_EUR"],
        marker="o",
        title="EUR cost of a USD payable under FX hedging strategies",
    )
    ax.set_xlabel("EUR/USD at payment date (USD per EUR)")
    ax.set_ylabel("Payment cost (EUR)")
    ax.grid(alpha=0.25)
    ax.figure.tight_layout()
    ax.figure.savefig(output_dir / "fx_hedging_costs.png", dpi=180)
    plt.close(ax.figure)


def main() -> None:
    exposure = FXExposure()
    table = build_scenario_table(exposure, [1.05, 1.10, 1.16, 1.22, 1.28])
    save_outputs(table, Path("outputs"))
    print(f"Theoretical 3M EUR/USD forward: {exposure.forward_rate:.4f}")
    print(f"Forward EUR budget: {exposure.forward_cost():,.2f}")
    print(table.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
