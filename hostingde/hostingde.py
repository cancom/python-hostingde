import json.decoder
from contextlib import contextmanager
from typing import Generator, Optional, Type, TypeVar

from requests import Response

import hostingde
from hostingde.exceptions import ApiException, ClientException
from hostingde.model import Model
from hostingde.model.filter import FilterElement
from hostingde.model.sort import SortConfiguration
from hostingde.session import HostingDeSession

T = TypeVar('T', bound='Model')


class HostingDeCore:
    def __init__(self, parent: 'HostingDeCore' = None):
        """
        Initialize a new Hosting.de API client.

        :param parent: The parent resource, used to retrieve session information. If not provided, a new session
                       is generated. WARNING: In this case, you must authenticate.
        """
        self.session = getattr(parent, 'session', parent) or self.new_session()

    def _post(self, *args, **kwargs):
        """
        Perform a post operation using your current session information.

        :param args: List parameters for post
        :param kwargs: Keyword parameters for post
        :return: The response of the post call
        """
        return self.session.post(*args, **kwargs)

    def _request(self, url: str, model: Optional[Model] = None, **kwargs: dict) -> Response:
        """
        Execute a new request, given an URL and a model. To generate a URL, you can use the _build_url() utility
        method.

        :param url: The URL resource to request
        :param model: The model to pass to the endpoint
        :param kwargs: additional keyword arguments to pass to requests.post()
        :return:
        """
        if model is None:
            response = self._post(url, **kwargs)
        else:
            response = self._post(url, json=model.to_json(), **kwargs)

        # Check if error occurred
        try:
            error_check = response.json()
            if error_check.get('status', 'error') == 'error':
                raise ApiException(error_check)
        except json.decoder.JSONDecodeError:
            raise ClientException('Error while reading response from server. Is your endpoint configured correctly?')

        return response

    def _instance(self, instance_type: Type[T], data: dict) -> T:
        """
        Reconstructs a model from the passed in result.

        :param instance_type: The instance type to be reconstructed.
        :param data: The data used to reconstruct the model
        :return: The parsed model
        """
        return instance_type.from_json(data, self)  # type: ignore

    def _bool(self, response: Response) -> bool:
        """
        Converts a response to a boolean. True, if the request succeeded, otherwise False. Note that a status of
        'pending' also returns False. You may want to use the _async method to wait for the job to complete.

        :param response: The response from the backend.
        :return:
        """
        return response.json().get('status') == 'success'

    def _build_uri(self, service: str, method: str) -> str:
        """
        Build a URL for the given service and method.

        :param service: The service of the method, e.g. 'dns'.
        :param method: The method endpoint for the result.
        :return: The finished URL for the resource
        """
        return self.session.build_path(service, "v1", "json", method)

    def _iter(
        self,
        url: str,
        instance_class: Type[T],
        filter: Optional[FilterElement] = None,
        limit: Optional[int] = None,
        sort: Optional[SortConfiguration] = None,
    ) -> 'hostingde.HostingDePaginator[T]':
        """
        Use the generic filtering and sorting API to paginate over results.

        :param url: The URL of the resources to paginate.
        :param instance_class: The expected response container
        :param filter: The filter to be applied to the query
        :param limit: The maximum number of items retrieved per call
        :param sort: The sorting of the resulting list
        :return: The iterator for the resultset
        """

        return hostingde.HostingDePaginator(self, instance_class, url, filter=filter, limit=limit, sort=sort)

    def login(self, url: str, token: str) -> None:
        """
        Perform a login.

        :param url: The URL of the endpoint
        :param token: The token to authorize requests
        """
        self.session.base_uri = url
        self.session.token_auth(token)

    def set_account_context(self, account_id: Optional[str]) -> None:
        """
        Sets the account context for this client.

        :param account_id: The account id
        :return:
        """
        self.session.set_account_context(account_id)

    @contextmanager
    def switch_account_context(self, account_id: str) -> Generator[None, None, None]:
        """
        Temporarily switch the account context for this client. After the context guard closes, the context is reset to
        the account that was used prior to the guard.

        :param account_id: The account id to switch to
        :return:
        """
        old_id: Optional[str] = self.session.get_account_context()

        self.session.set_account_context(account_id)

        yield

        self.session.set_account_context(old_id)

    @staticmethod
    def new_session() -> HostingDeSession:
        """
        Generates a new, unauthenticated session

        :return: The new session
        """
        return HostingDeSession()
