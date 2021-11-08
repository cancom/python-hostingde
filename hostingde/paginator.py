from dataclasses import dataclass, field
from typing import Generic, List, Optional, Type, TypeVar

from hostingde.exceptions import ClientException
from hostingde.hostingde import HostingDeCore
from hostingde.model import Model
from hostingde.model.filter import FilterElement
from hostingde.model.sort import SortConfiguration

R = TypeVar('R', bound="Model")


@dataclass
class PaginatedRequest(Model):
    """
    Represents a paginated request against a generic filtering and sorting API
    """

    filter: Optional[dict] = field(default=None)
    limit: Optional[int] = field(default=None)
    page: Optional[int] = field(default=None)
    sort: Optional[SortConfiguration] = field(default=None)


class HostingDePaginator(HostingDeCore, Generic[R]):
    def __init__(
        self,
        parent: HostingDeCore,
        instance_class: Type[R],
        url: str,
        count: Optional[int] = -1,
        limit: Optional[int] = 25,
        filter: Optional[FilterElement] = None,
        sort: Optional[SortConfiguration] = None,
    ):
        """
        Construct a new paginator.

        :param parent: The parent to get session details from
        :param instance_class: The instance class to create
        :param url: The URL of the resource to paginate over
        :param count: The total amount of entries to retrieve
        :param limit: The maximum number of entries to retrieve per API call
        :param filter: Filter the results based on a filter expression
        :param sort: Sort the results by a given field
        """
        super().__init__(parent)
        self.current_page = 1
        self.total_pages = -1
        self.results: List[R] = []
        self.limit = limit if limit is not None and limit > 0 else 25
        self.count = -1 if count is None or count <= 0 else count
        self.filter = filter
        self.sort = sort
        self.url = url
        self.count = count or -1
        self.instance_class = instance_class
        self._total_entries = -1

    def __iter__(self):
        """
        This object is a iterator itself.

        :return: Self
        """
        return self

    def _load_next(self) -> None:
        # No more results cached, and more available, load new results
        response = self._request(
            self.url,
            model=PaginatedRequest(
                filter=self.filter.to_filter_object() if self.filter is not None else None,
                limit=self.limit,
                page=self.current_page,
                sort=self.sort,
            ),
        )

        data = response.json().get('response', {})

        # if this was the first call, retrieve the amount of total pages
        if self.total_pages == -1:
            self.total_pages = data.get('totalPages', -1)
            self._total_entries = data.get('totalEntries', -1)

        self.current_page += 1

        # Extract and convert the results
        if len(data.get('data', [])) > 0:
            self.results.extend(map(lambda x: self._instance(self.instance_class, x), data.get('data', [])))

    def __next__(self):
        """
        Get the next result.

        :return: The next entry in the list
        """
        # Still requested more?
        if self.count == 0:
            raise StopIteration

        # If data is still available
        if len(self.results) > 0:
            self.count -= 1
            return self.results.pop(0)

        # Are there more pages to be retrieved?
        if self.total_pages < self.current_page and self.total_pages != -1:
            raise StopIteration

        self._load_next()

        # Extract and convert the results
        if len(self.results) > 0:
            self.count -= 1
            return self.results.pop(0)

        raise StopIteration

    def fetchall(self) -> List[R]:
        """
        Do not cache results, load all into memory.

        :return: The list of objects that this paginator generates
        """
        return list(self)

    def fetchone(self) -> R:
        """
        Only fetch a single resource from the API.

        :return: A single object returned from the API
        """
        try:
            return self.__next__()
        except StopIteration:
            raise ClientException('No entities found for given filter!')

    def __len__(self):
        """
        Length of items available
        :return: Number of entities
        """

        # If not yet loaded, prefetch data
        if self._total_entries == -1:
            self._load_next()

        return self._total_entries if self._total_entries >= 0 else 0
