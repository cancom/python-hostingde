import pytest

from python_hde.api import login


def test_success():
    client = login('endpoint', 'token')

    assert client is not None
    assert client.dns is not None
    assert client.dns.session == client.session


def test_no_endpoint_should_throw():
    with pytest.raises(Exception):
        login('', 'token')

    with pytest.raises(Exception):
        login(None, 'token')
