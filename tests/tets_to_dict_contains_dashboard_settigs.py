from src.models.app_settings import AppSettings


def test_to_dict_contains_dashboard_settings():

    settings = AppSettings(
        show_dashboard_kpis=False,
        show_dashboard_charts=False,
    )

    data = settings.to_dict()

    assert data["show_dashboard_kpis"] is False
    assert data["show_dashboard_charts"] is False
