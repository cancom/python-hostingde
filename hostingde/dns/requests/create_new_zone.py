from dataclasses import dataclass, field
from hostingde.model.zone_config import ZoneConfig
from hostingde.model import Model
from typing import List, Optional
from hostingde.model.record import Record


@dataclass
class CreateZoneRequest(Model):
    zone_config: ZoneConfig
    nameserver_set_id: Optional[str]
    use_default_nameserver_set: Optional[bool]
    records: List[Record] = field(default_factory=list)
