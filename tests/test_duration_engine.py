from src.core.estimation.duration_engine import (
    DurationEngine,
)


def test_calculate_basic():

    result = DurationEngine.calculate(
        estimated_hours=70,
    )

    assert result.estimated_hours == 70

    assert result.adjusted_hours == 70

    assert result.estimated_days == 10


def test_calculate_productivity():

    result = DurationEngine.calculate(
        estimated_hours=70,
        productivity_factor=2.0,
    )

    assert result.adjusted_hours == 35

    assert result.estimated_days == 5


def test_calculate_risk():

    result = DurationEngine.calculate(
        estimated_hours=70,
        risk_factor=2.0,
    )

    assert result.adjusted_hours == 140

    assert result.estimated_days == 20


def test_calculate_availability():

    result = DurationEngine.calculate(
        estimated_hours=70,
        availability_factor=0.5,
    )

    assert result.adjusted_hours == 140

    assert result.estimated_days == 20


def test_calculate_all_factors():

    result = DurationEngine.calculate(
        estimated_hours=70,
        productivity_factor=2.0,
        risk_factor=2.0,
        availability_factor=0.5,
    )

    # 70 / 2 * 2 / 0.5 = 140

    assert result.adjusted_hours == 140

    assert result.estimated_days == 20


def test_negative_hours():

    result = DurationEngine.calculate(
        estimated_hours=-10,
    )

    assert result.estimated_hours == 0

    assert result.adjusted_hours == 0

    assert result.estimated_days == 0


def test_productivity_lower_bound():

    result = DurationEngine.calculate(
        estimated_hours=10,
        productivity_factor=0,
    )

    assert result.productivity_factor == 0.1


def test_risk_lower_bound():

    result = DurationEngine.calculate(
        estimated_hours=10,
        risk_factor=0,
    )

    assert result.risk_factor == 1.0


def test_availability_lower_bound():

    result = DurationEngine.calculate(
        estimated_hours=10,
        availability_factor=0,
    )

    assert result.availability_factor == 0.1


def test_hours_to_days():

    assert DurationEngine.hours_to_days(70) == 10


def test_hours_to_days_negative():

    assert DurationEngine.hours_to_days(-100) == 0


def test_days_to_hours():

    assert DurationEngine.days_to_hours(10) == 70


def test_days_to_hours_negative():

    assert DurationEngine.days_to_hours(-10) == 0


def test_working_weeks():

    assert DurationEngine.working_weeks(25) == 5


def test_working_weeks_negative():

    assert DurationEngine.working_weeks(-25) == 0
