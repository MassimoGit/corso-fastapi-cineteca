"""La route di benvenuto: non legge il database, solo le Settings."""


def test_get_info_returns_name_and_version(client, test_settings):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"name": test_settings.app_name, "version": test_settings.app_version}
