from dataclasses import field
from typing import List

from marshmallow_dataclass import dataclass

from hostingde.model import Model
from hostingde.model.record import Record
from hostingde.model.zone_config import ZoneConfig


@dataclass
class Zone(Model):
    """
    A generic zone object used for responses.
    """

    zone_config: ZoneConfig
    records: List[Record] = field(default_factory=list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return f"Name: {self.zone_config.name}; Type: {self.zone_config.type.value}; Status: {self.zone_config.status}"
