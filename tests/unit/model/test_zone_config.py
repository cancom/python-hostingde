import pytest

from hostingde.model.zone_config import ZoneConfig, ZoneConfigType


def test_zone_config_constructor():
    zone_config = ZoneConfig(
        type=ZoneConfigType.NATIVE,
        id='asdawf',
        account_id='asfaegeg',
        status='success',
        name="cloud.de",
        name_unicode=None,
        email_address="test@example.org"
    )

    assert zone_config.type == ZoneConfigType.NATIVE
    assert zone_config.id == 'asdawf'
    assert zone_config.account_id == 'asfaegeg'
    assert zone_config.status == 'success'
    assert zone_config.name == "cloud.de"
    assert zone_config.name_unicode is None
    assert zone_config.email_address == "test@example.org"

    assert zone_config.zone_transfer_whitelist is None
    assert zone_config.last_change_date is None
    assert zone_config.soa_values is None


def test_zone_config_parse():
    data = dict(
        type="NATIVE",
        id='asdawf',
        accountId='asfaegeg',
        status='success',
        name="cloud.de",
        emailAddress="test@example.org"
    )

    zone_config = ZoneConfig.from_json(data)

    assert zone_config.type == ZoneConfigType.NATIVE
    assert zone_config.id == 'asdawf'
    assert zone_config.account_id == 'asfaegeg'
    assert zone_config.status == 'success'
    assert zone_config.name == "cloud.de"
    assert zone_config.name_unicode is None
    assert zone_config.email_address == "test@example.org"

    assert zone_config.zone_transfer_whitelist is None
    assert zone_config.last_change_date is None
    assert zone_config.soa_values is None


def test_zone_config_dump():

    zone_config = ZoneConfig(
        type=ZoneConfigType.NATIVE,
        id='asdawf',
        account_id='asfaegeg',
        status='success',
        name="cloud.de",
        name_unicode=None,
        email_address="test@example.org"
    )

    assert zone_config.to_json() == dict(
        type="NATIVE",
        id='asdawf',
        accountId='asfaegeg',
        status='success',
        name="cloud.de",
        emailAddress="test@example.org"
    )


def test_create_new_zone_master_ip_for_non_slave_should_throw():
    with pytest.raises(Exception):
        ZoneConfig.create_new_zone_config('cloud.de', ZoneConfigType.NATIVE, master_ip='127.0.0.1')

    with pytest.raises(Exception):
        ZoneConfig.create_new_zone_config('cloud.de', ZoneConfigType.MASTER, master_ip='127.0.0.1')


def test_create_new_zone_transfer_whitelist_only_for_master():
    with pytest.raises(Exception):
        ZoneConfig.create_new_zone_config('cloud.de', ZoneConfigType.NATIVE, zone_transfer_whitelist=[])

    with pytest.raises(Exception):
        ZoneConfig.create_new_zone_config('cloud.de', ZoneConfigType.SLAVE, zone_transfer_whitelist=[])


def test_create_new_zone_success():

    print(ZoneConfig.create_new_zone_config('cloud.de', ZoneConfigType.NATIVE))
