from datetime import datetime

from src.models.estimation_result import (
    EstimationResult,
)
from src.persistence.estimation_repository import (
    EstimationRepository,
)


def build_estimation():

    return EstimationResult(
        estimation_nom="HPC_Réaliste_V01",
        project_nom="HPC",
        profile_nom="Senior",
        scenario_nom="Réaliste",
        estimated_hours=100.0,
        estimated_days=15.0,
        estimated_cost=10000.0,
        risk_factor=1.0,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


def test_estimation_repository_exists():

    repo = EstimationRepository()

    assert repo is not None


def test_save_estimation():

    repo = EstimationRepository()

    estimation = build_estimation()

    repo.save(estimation)

    assert True


def test_count_returns_int():

    repo = EstimationRepository()

    result = repo.count()

    assert isinstance(
        result,
        int,
    )


def test_get_all_returns_list():

    repo = EstimationRepository()

    result = repo.get_all()

    assert isinstance(
        result,
        list,
    )


def test_get_unknown_estimation():

    repo = EstimationRepository()

    result = repo.get_estimation(-999999)

    assert result is None


def test_duplicate_unknown_estimation():

    repo = EstimationRepository()

    result = repo.duplicate_estimation(-999999)

    assert result is None


def test_save_and_read_estimation():

    repo = EstimationRepository()

    estimation = build_estimation()

    repo.save(estimation)

    estimations = repo.get_all()

    assert len(estimations) > 0

    assert any(e.project_nom == "HPC" for e in estimations)


def test_rename_unknown_estimation():

    repo = EstimationRepository()

    repo.rename_estimation(
        -999999,
        "TEST",
    )

    assert True


def test_delete_unknown_estimation():

    repo = EstimationRepository()

    repo.delete_estimation(-999999)

    assert True
