from python_hde.main import main
from python_hde.__version__ import __version__


def test_abc():
    assert main() == "test"
    assert __version__ is not None
