import tomllib

import pytest
from django.conf import settings
from django.test import override_settings
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_app_version_setting_then_matches_pyproject_version():
    with open(settings.BASE_DIR / "pyproject.toml", "rb") as pyproject_file:
        assert tomllib.load(pyproject_file)["project"]["version"] == settings.APP_VERSION


def test_api_root_base_then_is_v2():
    assert settings.API_ROOT_BASE == "v2/"


def test_health_then_returns_app_version():
    response = APIClient().get("/health/")
    assert response.json()["version"] == settings.APP_VERSION


@override_settings(GIT_COMMIT=None)
def test_health_without_git_commit_then_commit_is_null():
    response = APIClient().get("/health/")
    assert response.json()["commit"] is None


@override_settings(GIT_COMMIT="abc123")
def test_health_with_git_commit_then_returns_commit():
    response = APIClient().get("/health/")
    assert response.json()["commit"] == "abc123"
