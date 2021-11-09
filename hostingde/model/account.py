from dataclasses import dataclass
from typing import Any, Optional

from hostingde.model import Model


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

    def __init__(self, name: Optional[str], id: Optional[str], **kwargs: Any):
        """
        The Account object a object.
        :param name: Namw of this Account

        :param id: ID of this Account.
        """
        super().__init__(**kwargs)
        self.id: Optional[str] = id
        self.name: Optional[str] = name
