from dataclasses import dataclass, field
from typing import Any

from hostingde.model import Model


@dataclass
class SoaValues(Model):

    refresh: int = field(default=86400)
    retry: int = field(default=7200)
    expire: int = field(default=3600000)
    ttl: int = field(default=172800)
    negative_ttl: int = field(default=3600)

    def __init__(
        self,
        refresh: int = 86400,
        retry: int = 7200,
        expire: int = 3600000,
        ttl: int = 172800,
        negative_ttl: int = 3600,
        **kwargs: Any
    ):
        """
        The SOA values object contains the time (seconds) used in a zone's SOA record. The maximum number of seconds is
        31556926 which equals one year. Exceeding the maximum and uncercutting the minimum values will cause the request
        to be aborted and create an error.

        :param refresh: Refresh for the SOA record. Default: 86400, minimum: 3600.
        :param retry: Retry for the SOA record. Default: 7200, minimum: 600.
        :param expire: Expire for the SOA record. Default: 3600000, minimum: 86400.
        :param ttl: TTL for the SOA record. Default: 172800, minimum: 60.
        :param negative_ttl: Negative TTL for the SOA record. Default: 3600, minimum: 60.
        """
        super().__init__(**kwargs)
        self.refresh: int = refresh
        self.retry: int = retry
        self.expire: int = expire
        self.ttl: int = ttl
        self.negative_ttl: int = negative_ttl
