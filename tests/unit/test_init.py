from hostingde.__version__ import __version__ as version


def test_version_exists():
    assert version is not None
