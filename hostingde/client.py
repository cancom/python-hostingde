from hostingde.account.account import AccountClient
from hostingde.billing.billing import BillingClient
from hostingde.dns.dns import DnsClient
from hostingde.domain.domain import DomainClient
from hostingde.hostingde import HostingDeCore
from hostingde.ssl.ssl import SslClient


class HostingDeClient(HostingDeCore):
    """
    The main client.

    Separates the different problem domains by building clients in this class attributes.
    """

    def __init__(self):
        super().__init__()
        self.dns: DnsClient = DnsClient(self)
        self.domain: DomainClient = DomainClient(self)
        self.account: AccountClient = AccountClient(self)
        self.billing: BillingClient = BillingClient(self)
        self.ssl: SslClient = SslClient(self)
