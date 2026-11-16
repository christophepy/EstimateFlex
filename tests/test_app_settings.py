from src.models.app_settings import AppSettings


def test_dashboard_kpis_default_enabled():
    settings = AppSettings()
    assert settings.show_dashboard_kpis is True


def test_dashboard_charts_default_enabled():
    settings = AppSettings()
    assert settings.show_dashboard_charts is True


def test_to_dict_contains_dashboard_settings():
    settings = AppSettings(
        show_dashboard_kpis=False,
        show_dashboard_charts=False,
    )

    data = settings.to_dict()

    assert data["show_dashboard_kpis"] is False
    assert data["show_dashboard_charts"] is False


def test_from_dict_load_dashboard_settings():
    data = {
        "show_dashboard_kpis": False,
        "show_dashboard_charts": False,
    }

    settings = AppSettings.from_dict(data)

    assert settings.show_dashboard_kpis is False
    assert settings.show_dashboard_charts is False


def test_from_dict_missing_dashboard_settings():
    data = {
        "currency": "EUR",
    }

    settings = AppSettings.from_dict(data)

    assert settings.show_dashboard_kpis is True
    assert settings.show_dashboard_charts is True
