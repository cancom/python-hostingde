from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from marshmallow_enum import EnumField

from hostingde.exceptions import ClientException
from hostingde.model import Model
from hostingde.model.soa_values import SoaValues


class ZoneConfigType(Enum):
    """
    Available relations for conditional filters.
    """

    NATIVE = 'NATIVE'
    MASTER = 'MASTER'
    SLAVE = 'SLAVE'


@dataclass
class ZoneConfig(Model):
    """
    The ZoneConfig object defines a zone.

    type
        Valid types are NATIVE, MASTER, and SLAVE

    id
      ID of this zoneConfig. Ignored in zone create requests. Either id or name is required in all other
      requests.

    status
        Current status of the Zone

    name
        The zone name in ACE format. name is always required in zone create requests and all other requests
        if no id is provided. While you may use this property for a Unicode zone name, the responses will
        always contain the ACE encoded zone.

    name_unicode
        The zone name in Unicode. If it is left empty it will be filled automatically based on name.

    master_ip
        A valid IPv4 or IPv6 must be provided if the type is SLAVE. If the type is NATIVE or MASTER
        the field must be empty.

    email_address
        The hostmaster email address. Only relevant if the type is NATIVE or MASTER. If the field
        is left empty, the default is hostmaster@name.

    zone_transfer_whitelist
        List of IP addresses whitelisted for zone transfers. Only allowed if the type is
        MASTER. Must contain valid IPv4 or IPv6 addresses.

    last_change_date
        Date and time the zone was last modified

    soa_values
        Values for the SOA record of the zone. If it is left empty an SOA record with default values
        will be created.
    """

    id: Optional[str]
    account_id: Optional[str]
    status: Optional[str]
    name: Optional[str]
    name_unicode: Optional[str]
    dns_sec_mode: Optional[str]
    master_ip: Optional[str]
    email_address: Optional[str]
    zone_transfer_whitelist: Optional[List[str]]
    last_change_date: Optional[str]
    soa_values: Optional[SoaValues]
    type: ZoneConfigType = EnumField(ZoneConfigType)

    def __init__(
        self,
        type: ZoneConfigType,
        id: Optional[str] = None,
        account_id: Optional[str] = None,
        status: Optional[str] = None,
        name: Optional[str] = None,
        name_unicode: Optional[str] = None,
        master_ip: Optional[str] = None,
        email_address: Optional[str] = None,
        dns_sec_mode: Optional[str] = None,
        zone_transfer_whitelist: Optional[List[str]] = None,
        last_change_date: Optional[str] = None,
        soa_values: Optional[SoaValues] = None,
        **kwargs: dict,
    ):
        """
        The ZoneConfig object defines a zone.

        :param type: Valid types are NATIVE, MASTER, and SLAVE

        :param id: ID of this zoneConfig. Ignored in zone create requests. Either id or name is required in all other
                   requests.

        :param account_id: ID of the account that manages the zone. This property is never used in requests.

        :param status: Current status of the Zone

        :param name: The zone name in ACE format. name is always required in zone create requests and all other requests
                     if no id is provided. While you may use this property for a Unicode zone name, the responses will
                     always contain the ACE encoded zone.

        :param name_unicode: The zone name in Unicode. If it is left empty it will be filled automatically based on
                             name.

        :param master_ip: A valid IPv4 or IPv6 must be provided if the type is SLAVE. If the type is NATIVE or MASTER
                          the field must be empty.

        :param email_address: The hostmaster email address. Only relevant if the type is NATIVE or MASTER. If the field
                              is left empty, the default is hostmaster@name.

        :param zone_transfer_whitelist: List of IP addresses whitelisted for zone transfers. Only allowed if the type is
                                        MASTER. Must contain valid IPv4 or IPv6 addresses.

        :param last_change_date: Date and time the zone was last modified

        :param soa_values: Values for the SOA record of the zone. If it is left empty an SOA record with default values
                           will be created.
        """
        super().__init__(**kwargs)
        self.id: Optional[str] = id
        self.account_id: Optional[str] = account_id
        self.status: Optional[str] = status
        self.name: Optional[str] = name
        self.name_unicode: Optional[str] = name_unicode
        self.master_ip: Optional[str] = master_ip
        self.type: Optional[ZoneConfigType] = type
        self.email_address: Optional[str] = email_address
        self.zone_transfer_whitelist: Optional[List[str]] = zone_transfer_whitelist
        self.last_change_date: Optional[str] = last_change_date
        self.soa_values: Optional[SoaValues] = soa_values
        self.dns_sec_mode = dns_sec_mode

    @staticmethod
    def create_new_zone_config(
        name: str,
        type: ZoneConfigType,
        master_ip: Optional[str] = None,
        id: Optional[str] = None,
        email_address: str = None,
        soa_values: SoaValues = None,
        name_unicode: str = None,
        zone_transfer_whitelist: List[str] = None,
    ) -> 'ZoneConfig':
        if master_ip is not None and type != ZoneConfigType.SLAVE:
            raise ClientException("MasterIp can only be set if the type is SLAVE")

        if zone_transfer_whitelist is not None and type != ZoneConfigType.MASTER:
            raise ClientException("ZoneTransferWhiteList can only be used if the type is MASTER")

        if name is None:
            raise ClientException("No name for the zone was specified!")

        if type is None:
            raise ClientException("You must specify a zone type!")

        return ZoneConfig(
            id=id,
            name=name,
            master_ip=master_ip,
            name_unicode=name_unicode,
            email_address=email_address,
            soa_values=soa_values,
            type=type,
            zone_transfer_whitelist=zone_transfer_whitelist,
        )

    def __str__(self):
        return f"ZoneConfig for {self.name}"
