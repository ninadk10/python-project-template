"""Shared pytest fixtures available to all tests."""

from collections.abc import Generator

import pytest

from project_name.config import Settings


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Return a Settings instance configured for testing."""
    return Settings(
        env="test",
        log_level="DEBUG",
        data_dir="tests/fixtures/data",
    )


@pytest.fixture(autouse=True)
def reset_settings_cache() -> Generator[None, None, None]:
    """Clear the settings LRU cache between tests to avoid state leakage."""
    from project_name.config import get_settings
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()