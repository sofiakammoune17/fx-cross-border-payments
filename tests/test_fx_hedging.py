import pytest

from src.fx_hedging import FXExposure, build_scenario_table


def test_forward_rate_uses_interest_rate_parity():
    exposure = FXExposure()
    expected = 1.16 * (1 + 0.04 * 0.25) / (1 + 0.02 * 0.25)
    assert exposure.forward_rate == pytest.approx(expected)


def test_usd_payment_cost_falls_when_euro_strengthens():
    exposure = FXExposure()
    assert exposure.unhedged_cost(1.25) < exposure.unhedged_cost(1.05)


def test_forward_fixes_the_euro_budget():
    exposure = FXExposure()
    table = build_scenario_table(exposure, [1.05, 1.16, 1.28])
    assert table["Forward_EUR"].nunique() == 1


def test_option_caps_cost_before_premium():
    exposure = FXExposure()
    expected_cap = exposure.usd_notional / exposure.option_strike
    assert exposure.option_cost(1.05) == pytest.approx(expected_cap + exposure.option_premium_eur)


def test_invalid_hedge_ratio_is_rejected():
    with pytest.raises(ValueError):
        FXExposure(hedge_ratio=1.2)
