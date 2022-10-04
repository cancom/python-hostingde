from hostingde.model.domain import Domain


def test_parse_domain():
    data = {
        "name": "example.com",
        "transferLockEnabled": True,
        "contacts": [{
            "type": "owner",
            "contact": "123456789"
        }],
        "nameservers": [
            {"name": "ns1.example.com"}
        ]
    }

    result = Domain.from_json(data)

    assert result.name == "example.com"
    assert result.transfer_lock_enabled
    assert len(result.contacts) == 1
    assert len(result.nameservers) == 1


def test_dump_domain():
    data = {
        "name": "example.com",
        "transferLockEnabled": True,
        "contacts": [{
            "type": "owner",
            "contact": "123456789"
        }],
        "nameservers": [
            {"name": "ns1.example.com"}
        ]
    }

    result = Domain.from_json(data)

    assert result.to_json() == {
        "name": "example.com",
        "transferLockEnabled": True,
        "contacts": [{
            "type": "owner",
            "contact": "123456789"
        }],
        "nameservers": [
            {"name": "ns1.example.com", "ips": []}
        ]
    }
