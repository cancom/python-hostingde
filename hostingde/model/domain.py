from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Any

from marshmallow_enum import EnumField

from hostingde.model import Model


class DomainStatus(Enum):
    ordered = 'ordered'
    active = 'active'
    restorable = 'restorable'
    failed = 'failed'
    restricted = 'restricted'


class DomainContactRefType(Enum):
    owner = 'owner'
    tech = 'tech'
    admin = 'admin'
    zone = 'zone'


@dataclass
class DomainContactRef(Model):
    contact: str
    type: DomainContactRefType = EnumField(DomainContactRefType)

    def __init__(self, contact: str, type: DomainContactRefType, **kwargs):
        super().__init__(**kwargs)

        self.contact = contact
        self.type = type


@dataclass
class Nameserver(Model):
    def __init__(self, name: str, ips: Optional[List[str]] = None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.ips = ips

    name: str
    ips: List[str] = field(default_factory=list)


@dataclass
class Domain(Model):

    id: Optional[str]
    name: str
    name_unicode: Optional[str]
    account_id: Optional[str]
    transfer_lock_enabled:  bool
    auth_info: Optional[str]
    create_date: Optional[str]
    current_contract_period_end: Optional[str]
    next_contract_period_start: Optional[str]
    deletion_type: Optional[str]
    deletion_date: Optional[str]
    add_date: Optional[str]
    last_change_date: Optional[str]
    status: Optional[DomainStatus] = EnumField(DomainStatus)
    contacts: List[DomainContactRef] = field(default_factory=list)
    nameservers: List[Nameserver] = field(default_factory=list)

    def __init__(
            self,
            name: str,
            transfer_lock_enabled: bool = True,
            id: Optional[str] = None,
            name_unicode: Optional[str] = None,
            account_id: Optional[str] = None,
            status: Optional[DomainStatus] = None,
            auth_info: Optional[str] = None,
            contacts: Optional[List[DomainContactRef]] = None,
            nameservers: Optional[List[Nameserver]] = None,
            create_date: Optional[str] = None,
            current_contract_period_end: Optional[str] = None,
            next_contract_period_start: Optional[str] = None,
            deletion_type: Optional[str] = None,
            deletion_date: Optional[str] = None,
            add_date: Optional[str] = None,
            last_change_date: Optional[str] = None,
            **kwargs: Any
    ):
        """
        Represents a domain object
        :param name: Domain name. (Unicode or ASCII format). The name will always be returned in ASCII/ACE format.
        :param transfer_lock_enabled: 	If set to true, outgoing transfers will be blocked. Please keep in mind that
                                        not every TLD supports this feature.
        :param id: Domain ID
        :param name_unicode: Domain name in Unicode/international format
        :param account_id: The id of the account
        :param status: Domain status, 'ordered', 'active', 'restorable', 'failed'
        :param auth_info: 	The domain transfer authorisation code for this domain.
                            Only contains a value if transferLockEnabled is not set.
        :param contacts: 	List of contacts for this domain
        :param nameservers: List of name servers for this domain
        :param create_date: Date of domain creation. If the domain is transferred in and the registry does not support
                            getting the original creation date, it will be the date of the transfer.
        :param current_contract_period_end:  End date of current contract period
        :param next_contract_period_start: 	Start date of next contract period
        :param deletion_type: Removal mode (delete or withdraw). Empty when domain is not scheduled for removal.
        :param deletion_date: 	Date the domain is scheduled for deletion or withdrawal. Is empty if domain is not
                                scheduled for removal.
        :param add_date: Date and time this domain was created in or transferred into our system.
        :param last_change_date: Date and time of last modification of any domain data in our system.
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.name = name
        self.transfer_lock_enabled = transfer_lock_enabled
        self.id = id
        self.name_unicode = name_unicode
        self.account_id = account_id
        self.status = status
        self.auth_info = auth_info
        self.contacts = contacts or []
        self.nameservers = nameservers or []
        self.create_date = create_date
        self.current_contract_period_end = current_contract_period_end
        self.next_contract_period_start = next_contract_period_start
        self.deletion_type = deletion_type
        self.deletion_date = deletion_date
        self.add_date = add_date
        self.last_change_date = last_change_date


