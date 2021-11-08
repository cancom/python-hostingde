from hostingde.client import HostingDeClient
from hostingde.exceptions import ClientException


def login(base_url: str, token: str) -> HostingDeClient:
    """
    Entry point for the client. Builds and logs the user in.

    :param base_url: The base url for the backend, e.g. 'https://demo.routing.net/api'
    :param token: The token for authorization
    :return:
    """

    if base_url is None or base_url.strip() == "":
        raise ClientException('No base url set!')

    client = HostingDeClient()
    client.login(base_url, token)
    return client
