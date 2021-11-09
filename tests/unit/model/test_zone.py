from hostingde import HostingDeClient
from hostingde.model.zone import Zone


def test_zone_parse():
    data = dict(
        zoneConfig=dict(
            type="NATIVE",
            id='asdawf',
            accountId='asfaegeg',
            status='success',
            name="cloud.de",
            emailAddress="test@example.org",
        ),
        records=list(),
    )

    client = HostingDeClient()

    zone = Zone.from_json(data, client)

    assert zone.client == client
    assert zone.zone_config.client == client
