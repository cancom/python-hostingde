from typing import List, Optional

from hostingde.dns.requests.create_new_zone import CreateZoneRequest
from hostingde.dns.requests.delete_zone import DeleteZoneRequest
from hostingde.dns.requests.update_zone_request import UpdateZoneRequest
from hostingde.exceptions import ClientException
from hostingde.hostingde import HostingDeCore
from hostingde.job_waiter import AsynchronousClient, JobWaiter
from hostingde.model.filter import FilterElement
from hostingde.model.job import Job
from hostingde.model.record import Record
from hostingde.model.sort import SortConfiguration
from hostingde.model.zone import Zone
from hostingde.model.zone_config import ZoneConfig
from hostingde.paginator import HostingDePaginator


class DnsClient(HostingDeCore, AsynchronousClient):
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
        return self._build_uri('dns', method)

    def list_zones(
        self,
        limit: Optional[int] = None,
        filter: Optional[FilterElement] = None,
        sort: Optional[SortConfiguration] = None,
        *args: list,
        **kwargs: dict
    ) -> HostingDePaginator[Zone]:
        """
        Retrieves a list of Zone objects from the generic filtering and sorting API.

        +-------------------------+-------------------------------------------------------+
        | Field                   | Description                                           |
        +-------------------------+-------------------------------------------------------+
        | AccountId               | ID of the account to which the zone belongs           |
        +-------------------------+-------------------------------------------------------+
        | ZoneConfigId            | ID of the zoneConfig object                           |
        +-------------------------+-------------------------------------------------------+
        | ZoneName                | Zone name in ACE format                               |
        +-------------------------+-------------------------------------------------------+
        | ZoneNameUnicode         | Zone name in Unicode format                           |
        +-------------------------+-------------------------------------------------------+
        | ZoneMasterIp            | Master IP address of the zone                         |
        +-------------------------+-------------------------------------------------------+
        | ZoneType                | Zone type (“MASTER”, “NATIVE”, or “SLAVE”)            |
        +-------------------------+-------------------------------------------------------+
        | ZoneEmailAddress        | Email address of the zone                             |
        +-------------------------+-------------------------------------------------------+
        | ZoneLastChangeDate      | Time and date of last modification                    |
        +-------------------------+-------------------------------------------------------+
        | ZoneSoaRefresh          | SOA refresh interval of slaves (seconds)              |
        +-------------------------+-------------------------------------------------------+
        | ZoneSoaRetry            | SOA retry interval of slaves (seconds)                |
        +-------------------------+-------------------------------------------------------+
        | ZoneSoaExpire           | SOA deactivation timeout of slaves (seconds)          |
        +-------------------------+-------------------------------------------------------+
        | ZoneSoaTtl              | SOA time to live for negative caching (seconds)       |
        +-------------------------+-------------------------------------------------------+
        | ZoneIpv4Replacement     | Replacement value for IPv4 addresses in template      |
        +-------------------------+-------------------------------------------------------+
        | ZoneIpv6Replacement     | Replacement value for IPv6 addresses in template      |
        +-------------------------+-------------------------------------------------------+
        | ZoneMailIpv4Replacement | Replacement value for IPv4 mail addresses in template |
        +-------------------------+-------------------------------------------------------+
        | ZoneMailIpv6Replacement | Replacement value for IPv6 mail addresses in template |
        +-------------------------+-------------------------------------------------------+
        | TemplateName            | Name of template associated with zone                 |
        +-------------------------+-------------------------------------------------------+
        | TemplateId              | ID of template associated with zone                   |
        +-------------------------+-------------------------------------------------------+
        | RecordId                | ID of record in zone                                  |
        +-------------------------+-------------------------------------------------------+
        | RecordName              | Name of record in zone                                |
        +-------------------------+-------------------------------------------------------+
        | RecordType              | Type of record in zone                                |
        +-------------------------+-------------------------------------------------------+
        | RecordContent           | Content of record in zone                             |
        +-------------------------+-------------------------------------------------------+
        | RecordTtl               | Time to live (in seconds)                             |
        +-------------------------+-------------------------------------------------------+
        | RecordPriority          | Priority of record in zone (integer)                  |
        +-------------------------+-------------------------------------------------------+
        | RecordLastChangedate    | Date and time of last modification in zone            |
        +-------------------------+-------------------------------------------------------+

        :param limit: The limit of objects to retrieve per call. If not set, defaults to 25.
        :param filter: A filter that is applied to the query
        :param sort: Configuration how results are sorted.
        :return: An iterator that yields Zone objects.
        """

        uri = self._build_uri('dns', 'zonesFind')

        return self._iter(uri, Zone, filter, limit, sort)

    def list_zone_configs(
        self,
        limit: Optional[int] = None,
        filter: Optional[FilterElement] = None,
        sort: Optional[SortConfiguration] = None,
        *args: list,
        **kwargs: dict
    ) -> HostingDePaginator[ZoneConfig]:
        """
        Retrieves a list of ZoneConfig objects from the generic filtering and sorting API.

        +-------------------------+-----------------------------------------------------------+
        | Field                   | Description                                               |
        +-------------------------+-----------------------------------------------------------+
        | AccountId               | ID of the account that the zone belongs to                |
        +-------------------------+-----------------------------------------------------------+
        | ZoneConfigId            | ZoneConfig object ID                                      |
        +-------------------------+-----------------------------------------------------------+
        | ZoneName                | Zone name in ACE format                                   |
        +-------------------------+-----------------------------------------------------------+
        | ZoneNameUnicode         | Zone name in Unicode format                               |
        +-------------------------+-----------------------------------------------------------+
        | ZoneMasterIp            | Master IP address of the zone                             |
        +-------------------------+-----------------------------------------------------------+
        | ZoneType                | Zone type (“MASTER”, “NATIVE”, or “SLAVE”)                |
        +-------------------------+-----------------------------------------------------------+
        | ZoneEmailAddress        | Email address of hostmaster                               |
        +-------------------------+-----------------------------------------------------------+
        | ZoneLastChangeDate      | Date and time of last zone update                         |
        +-------------------------+-----------------------------------------------------------+
        | ZoneSoaRefresh          | SOA refresh interval of slaves (seconds)                  |
        +-------------------------+-----------------------------------------------------------+
        | ZoneSoaRetry            | SOA retry interval of slaves (seconds)                    |
        +-------------------------+-----------------------------------------------------------+
        | ZoneSoaExpire           | SOA deactivation timeout of slaves (seconds)              |
        +-------------------------+-----------------------------------------------------------+
        | ZoneSoaTtl              | SOA time to live for negative caching (seconds)           |
        +-------------------------+-----------------------------------------------------------+
        | ZoneIpv4Replacement     | Replacement value for ##IPv4## placeholder in template    |
        +-------------------------+-----------------------------------------------------------+
        | ZoneIpv6Replacement     | Replacement value for ##IPv6## placeholder in template    |
        +-------------------------+-----------------------------------------------------------+
        | ZoneMailIpv4Replacement | Replacement value for ##IPv4## mail addresses in template |
        +-------------------------+-----------------------------------------------------------+
        | ZoneMailIpv6Replacement | Replacement value for ##IPv6## mail addresses in template |
        +-------------------------+-----------------------------------------------------------+
        | TemplateName            | Name of template associated with zone                     |
        +-------------------------+-----------------------------------------------------------+
        | TemplateId              | ID of template associated with zone                       |
        +-------------------------+-----------------------------------------------------------+

        :param limit: The limit of objects to retrieve per call. If not set, defaults to 25.
        :param filter: A filter that is applied to the query
        :param sort: Configuration how results are sorted.
        :return: An iterator that yields Zone objects.
        """

        uri = self._build_uri('dns', 'zoneConfigsFind')

        return self._iter(uri, ZoneConfig, filter, limit, sort)

    def list_records(
        self,
        limit: Optional[int] = None,
        filter: Optional[FilterElement] = None,
        sort: Optional[SortConfiguration] = None,
        *args: list,
        **kwargs: dict
    ) -> HostingDePaginator[Record]:
        """
        Retrieves a list of Record objects from the generic filtering and sorting API.

        +----------------------+---------------------------------------------------------+
        | Field                | Description                                             |
        +----------------------+---------------------------------------------------------+
        | ZoneConfigId         | ID of the zoneConfig object to which the record belongs |
        +----------------------+---------------------------------------------------------+
        | RecordId             | Record object ID                                        |
        +----------------------+---------------------------------------------------------+
        | RecordName           | Name of the record                                      |
        +----------------------+---------------------------------------------------------+
        | RecordType           | Type of the record                                      |
        +----------------------+---------------------------------------------------------+
        | RecordContent        | Content of the record                                   |
        +----------------------+---------------------------------------------------------+
        | RecordTtl            | Time to live (in seconds)                               |
        +----------------------+---------------------------------------------------------+
        | RecordPriority       | Priority of the record (integer)                        |
        +----------------------+---------------------------------------------------------+
        | RecordLastChangeDate | Date and time of last modification                      |
        +----------------------+---------------------------------------------------------+

        :param limit: The limit of objects to retrieve per call. If not set, defaults to 25.
        :param filter: A filter that is applied to the query
        :param sort: Configuration how results are sorted.
        :return: An iterator that yields Zone objects.
        """

        uri = self._build_uri('dns', 'recordsFind')

        return self._iter(uri, Record, filter, limit, sort)

    def delete_zone(
        self, zone_config_id: Optional[str] = None, zone_name: Optional[str] = None, asynchronous: bool = None
    ) -> bool:
        """
        The complete zone, ie. the zoneConfig and all records, will be deleted.
        Either the ID or the name has to be provided. If both are set, an error will be returned.

        :param zone_config_id: The ID of the zone to delete
        :param zone_name: The name of the zone to delete
        :param asynchronous: Perform delete async. Synchronous is only supported for a given zone_config_id.
        :return: EmptyResponse
        """

        if zone_config_id is None and zone_name is None:
            raise ClientException('At least one parameter has to be provided.')

        if zone_config_id is not None and zone_name is not None:
            raise ClientException('Only one parameter must be provided: Either the name, or the id, but not both.')

        if zone_name and not asynchronous:
            raise ClientException('Deleting a zone synchronously by name is currently not supported!')

        url = self.build_uri('zoneDelete')
        self._request(url, DeleteZoneRequest(zone_config_id=zone_config_id, zone_name=zone_name))

        if not asynchronous and zone_config_id is not None:
            JobWaiter(self, zone_config_id).wait()

        return True

    def jobs_find(
        self,
        limit: Optional[int] = None,
        filter: Optional[FilterElement] = None,
        sort: Optional[SortConfiguration] = None,
        *args: list,
        **kwargs: dict
    ) -> HostingDePaginator[Job]:
        """
        Retrieves a list of Job objects from the generic filtering and sorting API.

        :param limit: The limit of objects to retrieve per call. If not set, defaults to 25.
        :param filter: A filter that is applied to the query
        :param sort: Configuration how results are sorted.
        :return: An iterator that yields ZoneConfig objects.
        """
        uri = self._build_uri('dns', 'jobsFind')

        return self._iter(uri, Job, filter, limit, sort)

    def update_zone(
        self,
        zone_config: ZoneConfig,
        records_to_add: Optional[List[Record]] = None,
        records_to_delete: Optional[List[Record]] = None,
        records_to_modify: Optional[List[Record]] = None,
        asynchronous: Optional[bool] = None,
    ) -> Zone:
        """
        You can use zoneUpdate to make adjustments to the zone's zoneConfig, to remove records, to add new records or
        to modify existing records.

        All records in recordsToAdd will be added to the zone, while all records in recordsToDelete will be deleted.
        All records in recordsToModify will be modified. If you insert a record that does not exist into recordsToDelete
        or recordsToModify, an error will occur.

        Existing records that are not contained in either list will not be changed.

        :param zone_config: zoneConfig to be updated
        :param records_to_add: Records to be added
        :param records_to_delete: Records to be modified
        :param records_to_modify: Records to be deleted
        :param asynchronous: Update the zone asynchronously. If not provided, defaults to synchronous mode.
        :return:
        """
        url = self.build_uri('zoneUpdate')

        response = self._request(
            url,
            UpdateZoneRequest(
                zone_config=zone_config,
                records_to_add=records_to_add,
                records_to_delete=records_to_delete,
                records_to_modify=records_to_modify,
            ),
        )

        zone = self._instance(Zone, response.json().get('response', {}))

        if not asynchronous and zone.zone_config.id is not None:
            JobWaiter(self, zone.zone_config.id).wait()

        return zone

    def create_zone(
        self,
        zone_config: ZoneConfig,
        records: List = None,
        nameserver_set_id: Optional[str] = None,
        use_default_nameserver_set: Optional[bool] = None,
        asynchronous: Optional[bool] = None,
    ) -> Zone:
        """
        To create a zone, you need at least a zoneConfig.

        A zone may be created manually or from a template. If you want to use a template, you have to at least provide
        a template ID in the zoneConfig's template values property. See template object for more details.

        See NameserverSet object for more details on using nameserver sets.

        :param zone_config: zoneConfig of the zone
        :param records: Records of the zone
        :param nameserver_set_id: NameserverSet to use for automatic creation of NS records. Default: 0
        :param use_default_nameserver_set: Use your account's default nameserver set. Default: false
        :param asynchronous: Create the zone asynchronously. If not provided, defaults to False (synchronous mode).
        :return:
        """
        if records is None:
            records = []

        url = self.build_uri('zoneCreate')

        response = self._request(
            url,
            CreateZoneRequest(
                zone_config=zone_config,
                records=records,
                nameserver_set_id=nameserver_set_id,
                use_default_nameserver_set=use_default_nameserver_set,
            ),
        )

        zone: Zone = self._instance(Zone, response.json().get('response', {}))

        if not asynchronous and zone.zone_config.id is not None:
            JobWaiter(self, zone.zone_config.id).wait()

        return zone
