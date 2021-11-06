from dataclasses import dataclass
from typing import Optional

from python_hde.model import Model


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

    def __init__(self, name: Optional[str], id: Optional[str]):
        """
        The Account object a object.
        :param name: Namw of this Account

        :param id: ID of this Account.
        """
        self.id: Optional[str] = id
        self.name: Optional[str] = name
