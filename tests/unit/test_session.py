import pytest
import responses
from requests import PreparedRequest, Response

from python_hde.session import HostingDeSession


def test_session_create():
    session = HostingDeSession()

    assert session is not None
    assert session.base_uri is None
    assert session.auth is None


def test_session_set_parameters():
    session = HostingDeSession()

    session.set_endpoint('https://example.com')
    assert session.base_uri is not None

    session.token_auth('random')
    assert session.auth is not None


def test_session_build_path():
    session = HostingDeSession()

    session.set_endpoint('https://example.com')
    session.token_auth('demotoken')

    assert session.build_path() == 'https://example.com'
    assert session.build_path('test') == 'https://example.com/test'
    assert session.build_path('test', 'v1', 'json') == 'https://example.com/test/v1/json'


def test_session_build_path_no_base_path_should_throw():
    session = HostingDeSession()
    session.token_auth('demotoken')

    with pytest.raises(Exception):
        session.build_path('demo')


@responses.activate
def test_auth_injection_with_body():
    session = HostingDeSession()
    session.set_endpoint('https://example.com')
    session.token_auth('demotoken')

    def echo_callback(r: PreparedRequest):
        return 200, r.headers, r.body.decode('utf-8')

    responses.add_callback('POST', 'https://example.com', echo_callback)

    response: Response = session.post('https://example.com', json={})

    assert response.json().get('authToken') == 'demotoken'


@responses.activate
def test_auth_injection_without_body():
    session = HostingDeSession()
    session.set_endpoint('https://example.com')
    session.token_auth('demotoken')

    def echo_callback(r: PreparedRequest):
        return 200, r.headers, r.body.decode('utf-8')

    responses.add_callback('POST', 'https://example.com', echo_callback)

    response: Response = session.post('https://example.com')

    assert response.json().get('authToken') == 'demotoken'
