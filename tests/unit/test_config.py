"""Unit tests for config module."""

import pytest

from project_name.config import Settings


def test_default_settings():
    settings = Settings()
    assert settings.env == "development"
    assert settings.log_level == "INFO"


def test_log_level_validation():
    with pytest.raises(ValueError):
        Settings(log_level="INVALID")


def test_is_production_false_by_default():
    settings = Settings()
    assert settings.is_production is False


def test_is_production_true():
    settings = Settings(env="production")
    assert settings.is_production is True