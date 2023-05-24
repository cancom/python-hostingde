from typing import Optional

from hostingde.paginator import HostingDePaginator
from hostingde.hostingde import HostingDeCore
from hostingde.model.billing import DomainPrice
from hostingde.model.filter import FilterElement
from hostingde.model.sort import SortConfiguration
from hostingde.model.ssl import Certificate


class SslClient(HostingDeCore):
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
        return self._build_uri('ssl', method)

    def certificates_find(
        self,
        limit: Optional[int] = None,
        filter: Optional[FilterElement] = None,
        sort: Optional[SortConfiguration] = None,
        page: Optional[int] = None,
        *args: list,
        **kwargs: dict
    ) -> HostingDePaginator[Certificate]:
        """
        List SSL certificates

        :param limit: The limit of objects to retrieve per call. If not set, defaults to 25.
        :param filter: A filter that is applied to the query
        :param sort: Configuration how results are sorted.
        :param page: The page to retrieve. If limit is unset, 25 items will be retrieved.
        :return: An iterator that yields Zone objects.
        """

        uri = self._build_uri('ssl', 'certificatesFind')

        return self._iter(uri, Certificate, filter, limit, sort, page)
