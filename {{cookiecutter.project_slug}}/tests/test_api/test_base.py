from {{cookiecutter.project_slug}}.app.version import __version__


def test_get_version(test_client):
    response = test_client.get("/api/v1/version")
    assert response.status_code == 200
    assert response.json() == {"version": __version__}
