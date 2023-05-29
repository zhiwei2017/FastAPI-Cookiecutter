from {{cookiecutter.project_slug}}.app.schemas.base import VersionResponse


def test_versionresponse():
    vr = VersionResponse(version="1.0.0")
    assert vr.version == "1.0.0"
