from python_hde.account.account import AccountClient
from python_hde.dns.dns import DnsClient
from python_hde.hostingde import HostingDeCore


class HostingDeClient(HostingDeCore):
    """
    The main client.

    Separates the different problem domains by building clients in this class attributes.
    """

    def __init__(self):
        super().__init__()
        self.dns: DnsClient = DnsClient(self)
        self.account: AccountClient = AccountClient(self)
