from dataclasses import dataclass
from typing import Any, Optional

from hostingde.model import Model


@dataclass
class DomainSettings(Model):
    default_contact_admin_id: str
    default_contact_owner_id: str
    default_contact_tech_id: str
    default_contact_zone_id: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class Account(Model):
    """
    Name
    Name of the Account

    id
    ID of this Account.
    """

    name: Optional[str]
    id: Optional[str]
    domain_settings: Optional[DomainSettings]

    def __init__(
            self,
            name: Optional[str],
            id: Optional[str],
            domain_settings: Optional[DomainSettings] = None,
            **kwargs: Any
    ):
        """
        The Account object a object.
        :param name: Namw of this Account

        :param id: ID of this Account.
        """
        super().__init__(**kwargs)
        self.id: Optional[str] = id
        self.name: Optional[str] = name
        self.domain_settings = domain_settings
