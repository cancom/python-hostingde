import json
from typing import Optional

import requests as requests
from requests import auth, models

from hostingde.exceptions import ClientException


class HostingDeAuth(auth.AuthBase):
    """
    A Auth injector for the hosting.de API. Injects the token and (optionally) the account into the request body.
    """

    def __init__(self, token: str, token_field: str = 'authToken', account_id: str = None):
        super().__init__()
        self.token = token
        self.token_field = token_field
        self.account_id = account_id

    def __call__(self, r: models.PreparedRequest) -> models.PreparedRequest:
        """
        Rewrite the request to include the auth token.

        :param r: A prepared request
        :return: A modified request that contains the authorization
        """

        # Always inject the token
        if r.body is None:
            request = {}
        else:
            request = json.loads(r.body)

        request[self.token_field] = self.token

        if self.account_id is not None:
            request['ownerAccountId'] = self.account_id

        r.body = json.dumps(request).encode('utf-8')
        return r


class HostingDeSession(requests.Session):
    """
    Custom session implementation contains the Hosting.de authorization implementation
    """

    def __init__(self: 'HostingDeSession'):
        super().__init__()
        self.base_uri: Optional[str] = None

    def build_path(self, *args, **kwargs):
        """
        Build the url path to the resource queried.

        :param args: A path to the resource
        :param kwargs: Optionally, you can provide the base_uri to override the default implementation
        :return:
        """
        uri = [kwargs.get('base_uri') or self.base_uri]

        if uri[0] is None:
            raise ClientException('No endpoint URL set.')

        uri.extend(args)
        return "/".join(uri)

    def set_endpoint(self, url: str) -> None:
        """
        Set the base URL for this session

        :param url: The base url to use for all requests
        :return:
        """
        self.base_uri = url

    def token_auth(self, token: str) -> None:
        """
        Authenticate using a token

        :param token: The token to use for authentication
        :return:
        """
        self.auth = HostingDeAuth(token)

    def set_account_context(self, account_id: Optional[str]) -> None:
        """
        Switch context to subaccount

        :param account_id: The account id of the subaccount.
        :return:
        """
        if isinstance(self.auth, HostingDeAuth):
            self.auth.account_id = account_id
        else:
            raise ClientException('Subaccount could not be attached to request')

    def get_account_context(self) -> Optional[str]:
        """
        Get the current account used for requests.

        :return: The account id
        """
        if isinstance(self.auth, HostingDeAuth):
            return self.auth.account_id
        else:
            raise ClientException('Subaccount could not be attached to request')
