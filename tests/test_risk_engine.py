from src.core.risk.risk_engine import (
    RiskEngine,
    RiskResult,
)


def test_calculate_low_risk():

    result = RiskEngine.calculate(
        planning_risk=1,
        scope_risk=1,
        technical_risk=1,
    )

    assert isinstance(
        result,
        RiskResult,
    )

    assert result.score == 1.0

    assert result.factor == 1.1


def test_calculate_medium_risk():

    result = RiskEngine.calculate(
        planning_risk=2,
        scope_risk=2,
        technical_risk=2,
    )

    assert result.score == 2.0

    assert result.factor == 1.2


def test_calculate_high_risk():

    result = RiskEngine.calculate(
        planning_risk=3,
        scope_risk=3,
        technical_risk=3,
    )

    assert result.score == 3.0

    assert result.factor == 1.3


def test_calculate_mixed_risk():

    result = RiskEngine.calculate(
        planning_risk=1,
        scope_risk=2,
        technical_risk=3,
    )

    assert result.score == 2.0

    assert result.factor == 1.2


def test_score_rounding():

    result = RiskEngine.calculate(
        planning_risk=1,
        scope_risk=2,
        technical_risk=2,
    )

    assert result.score == 1.67

    assert result.factor == 1.17


def test_return_type():

    result = RiskEngine.calculate(
        planning_risk=2,
        scope_risk=1,
        technical_risk=3,
    )

    assert hasattr(
        result,
        "score",
    )

    assert hasattr(
        result,
        "factor",
    )


def test_factor_greater_than_one():

    result = RiskEngine.calculate(
        planning_risk=5,
        scope_risk=5,
        technical_risk=5,
    )

    assert result.factor > 1.0


def test_zero_risk():

    result = RiskEngine.calculate(
        planning_risk=0,
        scope_risk=0,
        technical_risk=0,
    )

    assert result.score == 0.0

    assert result.factor == 1.0
