import pytest


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "integration: marks tests as requiring live API credentials "
        "(deselect with '-m \"not integration\"')",
    )
