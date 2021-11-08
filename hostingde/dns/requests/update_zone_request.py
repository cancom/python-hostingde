from dataclasses import dataclass, field
from typing import List, Optional

from hostingde.model import Model
from hostingde.model.record import Record
from hostingde.model.zone_config import ZoneConfig


def record_list() -> List[Record]:
    return []


@dataclass
class UpdateZoneRequest(Model):

    zone_config: ZoneConfig
    records_to_add: Optional[List[Record]] = field(default_factory=record_list)
    records_to_modify: Optional[List[Record]] = field(default_factory=record_list)
    records_to_delete: Optional[List[Record]] = field(default_factory=record_list)
