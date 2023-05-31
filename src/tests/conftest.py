import pytest


@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    """
    This fixture ensures that generated roadmaps end up in correct path,
    no matter from which path tests are executed.
    """
    monkeypatch.chdir(request.fspath.dirname)


@pytest.fixture(scope="session")
def operating_system_ubuntu():
    """
    This fixture can be used as test argument to provide string of used OS `Ubuntu`.
    """
    return "Ubuntu"
