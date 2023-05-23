from hostingde.hostingde import HostingDeCore
from hostingde.model.billing import DomainPrice


class BillingClient(HostingDeCore):
    def __init__(self, parent: HostingDeCore):
        """
        Construct a new Account client

        :param parent: The parent to retrieve the session from
        """
        super().__init__(parent)

    def build_uri(self, method: str) -> str:
        """
        Utility method to easily construct URLs for this service.

        :param method: The method within this service
        :return: The URL string
        """
        return self._build_uri('billing', method)

    def price_list_domains(self):
        """
        Get the price list of all domains

        :return:
        """

        uri = self._build_uri('billing', 'priceListDomains')

        response = self._request(uri, None)

        data = response.json().get('responses', {})
        print(data[3])

        return [self._instance(DomainPrice, x) for x in data]
