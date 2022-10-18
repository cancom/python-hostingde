from typing import Optional, List, Union

from hostingde.domain.requests.check_availability import CheckAvailabilityRequest, CheckAvailabilityResponse
from hostingde.domain.requests.register_domain import RegisterDomainRequest
from hostingde.model.domain_contact import DomainContact
from hostingde.paginator import HostingDePaginator
from hostingde.hostingde import HostingDeCore
from hostingde.job_waiter import AsynchronousClient, JobWaiter
from hostingde.model.domain import Domain, Nameserver, DomainContactRef
from hostingde.model.filter import FilterElement
from hostingde.model.job import Job
from hostingde.model.sort import SortConfiguration


class DomainClient(HostingDeCore, AsynchronousClient):

    def __init__(self, parent: HostingDeCore):
        """
        Construct a new client

        :param parent: The parent to retrieve the session from
        """
        super().__init__(parent)

    def build_uri(self, method: str) -> str:
        """
        Utility method to easily construct URLs for this service.

        :param method: The method within this service
        :return: The URL string
        """
        return self._build_uri('domain', method)

    def jobs_find(
        self,
        limit: Optional[int] = None,
        filter: Optional[FilterElement] = None,
        sort: Optional[SortConfiguration] = None,
        page: Optional[int] = None,
        *args: list,
        **kwargs: dict
    ) -> HostingDePaginator[Job]:
        """
        Retrieves a list of Job objects from the generic filtering and sorting API.

        :param limit: The limit of objects to retrieve per call. If not set, defaults to 25.
        :param filter: A filter that is applied to the query
        :param sort: Configuration how results are sorted.
        :param page: The page to retrieve. If limit is unset, 25 items will be retrieved.
        :return: An iterator that yields ZoneConfig objects.
        """
        uri = self._build_uri('domain', 'jobsFind')

        return self._iter(uri, Job, filter, limit, sort, page)

    def check_domain_name_availability(self, domain_names: Union[str, List[str]]) -> List[CheckAvailabilityResponse]:
        uri = self.build_uri('domainStatus')

        if type(domain_names) == str:
            domain_names = [domain_names]

        response = self._request(
            uri,
            CheckAvailabilityRequest(domain_names=domain_names)
        )

        data = response.json().get('responses', [])

        return list(map(lambda x: self._instance(CheckAvailabilityResponse, x), data))

    def list_domains(
        self,
        limit: Optional[int] = None,
        filter: Optional[FilterElement] = None,
        sort: Optional[SortConfiguration] = None,
        page: Optional[int] = None,
        *args: list,
        **kwargs: dict
    ) -> HostingDePaginator[Domain]:
        """
        Retrieves a list of Domain objects from the generic filtering and sorting API.

        :param limit: The limit of objects to retrieve per call. If not set, defaults to 25.
        :param filter: A filter that is applied to the query
        :param sort: Configuration how results are sorted.
        :param page: The page to retrieve. If limit is unset, 25 items will be retrieved.
        :return: An iterator that yields Zone objects.
        """

        uri = self._build_uri('domain', 'domainsFind')

        return self._iter(uri, Domain, filter, limit, sort, page)

    def list_contacts(
        self,
        limit: Optional[int] = None,
        filter: Optional[FilterElement] = None,
        sort: Optional[SortConfiguration] = None,
        page: Optional[int] = None,
        *args: list,
        **kwargs: dict
    ) -> HostingDePaginator[DomainContact]:
        """
        Retrieves a list of Domain objects from the generic filtering and sorting API.

        :param limit: The limit of objects to retrieve per call. If not set, defaults to 25.
        :param filter: A filter that is applied to the query
        :param sort: Configuration how results are sorted.
        :param page: The page to retrieve. If limit is unset, 25 items will be retrieved.
        :return: An iterator that yields Zone objects.
        """

        uri = self._build_uri('domain', 'contactsFind')

        return self._iter(uri, DomainContact, filter, limit, sort, page)

    def register_domain(
        self,
        name: str,
        contacts: List[DomainContactRef],
        nameservers: List[Nameserver],
        transfer_lock_enabled=True,
        asynchronous: Optional[bool] = None,
    ) -> Domain:
        """
        In order to create a domain, you need to send a domainCreate request. This request takes one parameter domain
        which contains all required information of a domain object.

        :param name:
        :param contacts:
        :param nameservers:
        :param transfer_lock_enabled:
        :param asynchronous:
        :return:
        """
        url = self.build_uri('domainCreate')

        response = self._request(
            url,
            RegisterDomainRequest(
                domain=Domain(
                    name=name,
                    contacts=contacts,
                    nameservers=nameservers,
                    transfer_lock_enabled=transfer_lock_enabled
                )
            ),
        )

        domain: Domain = self._instance(Domain, response.json().get('response', {}))

        if not asynchronous and domain.id is not None:
            JobWaiter(self, domain.id, 'domainCreate').wait()

        return domain