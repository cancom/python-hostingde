from dataclasses import dataclass
from typing import Optional

from hostingde.model import Model


@dataclass
class DeleteZoneRequest(Model):

    zone_config_id: Optional[str]
    zone_name: Optional[str]
