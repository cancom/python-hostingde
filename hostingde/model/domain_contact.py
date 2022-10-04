from dataclasses import dataclass
from enum import Enum
from typing import Optional, List

from hostingde.exceptions import ContextConditionException
from hostingde.model import Model


class DomainContactType(Enum):
    person = 'person'
    org = 'org'
    role = 'role'


@dataclass
class DomainContact(Model):
    id: Optional[str]
    handle: Optional[str]
    type: DomainContactType
    name: str
    organization: Optional[str]
    street: List[str]
    postal_code: Optional[str]
    city: str
    state: str
    country: str
    email_address: str
    phone_number: str
    fax_number: Optional[str]
    sip_uri: Optional[str]
    hidden: Optional[bool]
    usable_by_subaccount: Optional[bool]
    add_date: Optional[str]
    last_change_date: Optional[str]

    def __init__(
        self,
        type: DomainContactType,
        name: str,
        street: List[str],
        city: str,
        country: str,
        email_address: str,
        phone_number: str,
        id: Optional[str] = None,
        handle: Optional[str] = None,
        organization: Optional[str] = None,
        postal_code: Optional[str] = None,
        fax_number: Optional[str] = None,
        sip_uri: Optional[str] = None,
        hidden: bool = False,
        usable_by_subaccount: bool = False,
        add_date: Optional[str] = None,
        last_change_date: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.type = type
        self.name = name
        self.street = street
        self.city = city
        self.country = country
        self.email_address = email_address
        self.phone_number = phone_number
        self.id = id
        self.handle = handle
        self.organization = organization
        self.postal_code = postal_code
        self.fax_number = fax_number
        self.sip_uri = sip_uri
        self.hidden = hidden
        self.usable_by_subaccount = usable_by_subaccount
        self.add_date = add_date
        self.last_change_date = last_change_date

        if self.type == DomainContactType.org and not self.organization:
            raise ContextConditionException('An organization contact requires the "organization" field to be set.')
