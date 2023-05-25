from dataclasses import dataclass
from typing import Optional

from hostingde.model import Model


@dataclass
class Certificate(Model):
    account_id: str
    add_date: str
    auto_renew: bool
    brand: str
    cancelable_until: Optional[str]
    common_name: str
    end_date: Optional[str]
    external_order_id: str
    id: str
    intermediate_cert: str
    is_managed: bool
    last_change_date: str
    order_status: str
    product: str
    product_code: str
    renew_date: Optional[str]
    root_cert: str
    serial_number: str
    server_cert: str
    start_date: Optional[str]
    status: str
    validation_level: str
    validity_span_month: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)