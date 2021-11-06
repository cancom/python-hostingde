from dataclasses import dataclass, field
from typing import List

from python_hde.model import Model
from python_hde.model.record import Record
from python_hde.model.zone_config import ZoneConfig


@dataclass
class Zone(Model):
    """
    A generic zone object used for responses.
    """

    zone_config: ZoneConfig
    records: List[Record] = field(default_factory=list)

    def __str__(self):
        return f"Name: {self.zone_config.name}; Type: {self.zone_config.type.value}; Status: {self.zone_config.status}"
