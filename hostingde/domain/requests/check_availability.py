from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from marshmallow_enum import EnumField

from hostingde.model import Model


class CheckAvailabilityStatus(Enum):
    alreadyRegistered = 'alreadyRegistered'
    registered = 'registered'
    nameContainsForbiddenCharacter = 'nameContainsForbiddenCharacter'
    available = 'available'
    suffixDoesNotExist = 'suffixDoesNotExist'
    suffixCannotBeRegistered = 'suffixCannotBeRegistered'
    canNotCheck = 'canNotCheck'
    unknown = 'unknown'


@dataclass
class CheckAvailabilityRequest(Model):
    domain_names: List[str]


@dataclass
class CheckAvailabilityResponse(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    domain_name: str
    domain_name_unicode: str
    domain_suffix: str
    transfer_method: Optional[str]
    status: CheckAvailabilityStatus = EnumField(CheckAvailabilityStatus)
