from typing import Optional

from hostingde.hostingde import HostingDeCore
from hostingde.model.account import Account
from hostingde.model.filter import FilterElement
from hostingde.model.sort import SortConfiguration
from hostingde.paginator import HostingDePaginator


class AccountClient(HostingDeCore):
    def __init__(self, parent: HostingDeCore):
        """
        Construct a new Account client

        :param parent: The parent to retrieve the session from
        """
        super().__init__(parent)

    def build_uri(self, method: str) -> str:
        """
        Utility method to easily construct URLs for this service.

        :param method: The method within this service
        :return: The URL string
        """
        return self._build_uri('account', method)

    def list_subaccounts_names(
        self,
        limit: Optional[int] = None,
        filter: Optional[FilterElement] = None,
        sort: Optional[SortConfiguration] = None,
        *args: list,
        **kwargs: dict
    ) -> HostingDePaginator[Account]:
        """
        List subaccounts for the current context.

        :param limit: The limit of objects to retrieve per call. If not set, defaults to 25.
        :param filter: A filter that is applied to the query
        :param sort: Configuration how results are sorted.
        :return: An iterator that yields Zone objects.
        """

        uri = self._build_uri('account', 'subaccountsFind')

        return self._iter(uri, Account, filter, limit, sort)
