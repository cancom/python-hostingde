from hostingde.model.soa_values import SoaValues


def test_soa_constructor():
    soa: SoaValues = SoaValues(
        refresh=23,
        retry=213,
        expire=25,
        ttl=12566,
        negative_ttl=2
    )

    assert soa.refresh == 23
    assert soa.retry == 213
    assert soa.expire == 25
    assert soa.ttl == 12566
    assert soa.negative_ttl == 2


def test_soa_parse():
    data = dict(
        refresh=23,
        retry=213,
        expire=25,
        ttl=12566,
        negativeTtl=2
    )

    soa = SoaValues.from_json(data)

    assert soa.refresh == 23
    assert soa.retry == 213
    assert soa.expire == 25
    assert soa.ttl == 12566
    assert soa.negative_ttl == 2


def test_soa_dump():
    soa: SoaValues = SoaValues(
        refresh=23,
        retry=213,
        expire=25,
        ttl=12566,
        negative_ttl=2
    )

    assert soa.to_json() == dict(
        refresh=23,
        retry=213,
        expire=25,
        ttl=12566,
        negativeTtl=2
    )
