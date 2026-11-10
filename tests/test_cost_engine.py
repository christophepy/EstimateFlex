from src.core.estimation.cost_engine import (
    CostEngine,
)


def test_calculate_basic():

    result = CostEngine.calculate(
        estimated_hours=70,
        daily_rate=700,
    )

    assert result.estimated_hours == 70

    assert result.estimated_days == 10

    assert result.base_cost == 7000

    assert result.final_cost == 7000


def test_calculate_with_risk():

    result = CostEngine.calculate(
        estimated_hours=70,
        daily_rate=700,
        risk_factor=1.5,
    )

    assert result.base_cost == 7000

    assert result.final_cost == 10500


def test_calculate_negative_hours():

    result = CostEngine.calculate(
        estimated_hours=-10,
        daily_rate=700,
    )

    assert result.estimated_hours == 0


def test_calculate_negative_rate():

    result = CostEngine.calculate(
        estimated_hours=10,
        daily_rate=-500,
    )

    assert result.daily_rate == 0

    assert result.base_cost == 0


def test_calculate_risk_lower_than_one():

    result = CostEngine.calculate(
        estimated_hours=70,
        daily_rate=700,
        risk_factor=0.5,
    )

    assert result.risk_factor == 1.0


def test_from_days():

    result = CostEngine.from_days(
        estimated_days=10,
        daily_rate=700,
    )

    assert result.estimated_days == 10

    assert result.base_cost == 7000


def test_from_days_negative():

    result = CostEngine.from_days(
        estimated_days=-5,
        daily_rate=700,
    )

    assert result.estimated_hours == 0

    assert result.base_cost == 0


def test_margin():

    assert (
        CostEngine.margin(
            selling_price=12000,
            estimated_cost=10000,
        )
        == 2000
    )


def test_margin_negative():

    assert (
        CostEngine.margin(
            selling_price=8000,
            estimated_cost=10000,
        )
        == -2000
    )


def test_margin_rate():

    assert (
        CostEngine.margin_rate(
            selling_price=12000,
            estimated_cost=9000,
        )
        == 25.0
    )


def test_margin_rate_zero_price():

    assert (
        CostEngine.margin_rate(
            selling_price=0,
            estimated_cost=1000,
        )
        == 0.0
    )


def test_margin_rate_negative_price():

    assert (
        CostEngine.margin_rate(
            selling_price=-100,
            estimated_cost=1000,
        )
        == 0.0
    )
