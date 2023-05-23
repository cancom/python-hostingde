from dataclasses import dataclass, field
from typing import Optional

from hostingde.model import Model


@dataclass
class ExchangeRatio(Model):
    base_currency: str
    currency: str
    exchange_date: str
    exchange_ratio: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

@dataclass
class DomainPrice(Model):
    create: int
    create_duration: int
    currency: str
    domain_suffix: str
    owner_change: Optional[int]
    period_of_notice: int
    renew: int
    renew_duration: int
    restore: Optional[int]
    transfer: Optional[int]
    transfer_duration: Optional[int]
    update: int
    vat_rate: int
    exchange_ratio: Optional[ExchangeRatio]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
