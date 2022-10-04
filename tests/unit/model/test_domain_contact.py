import pytest

from hostingde.exceptions import ContextConditionException
from hostingde.model.domain_contact import DomainContact, DomainContactType


def test_parse_domain_contact():
    data = {
        "type": "person",
        "name": "Mr. Test",
        "street": ["DisneyLand"],
        "postalCode": "012345",
        "state": "BER",
        "city": "Aachen",
        "country": "de",
        "emailAddress": "me@example.com",
        "phoneNumber": "+1 1234 6859321",
    }

    result = DomainContact.from_json(data)

    assert result.type == DomainContactType.person
    assert result.name == "Mr. Test"
    assert len(result.street) == 1
    assert result.postal_code == '012345'
    assert result.state == "BER"
    assert result.country == "de"
    assert result.email_address == "me@example.com"
    assert result.phone_number == "+1 1234 6859321"


def test_domain_contact_to_json():
    data = {
        "type": "person",
        "name": "Mr. Test",
        "street": ["DisneyLand"],
        "postalCode": "012345",
        "state": "BER",
        "country": "de",
        "city": "Aachen",
        "emailAddress": "me@example.com",
        "phoneNumber": "+1 1234 6859321",
    }

    result = DomainContact.from_json(data)

    assert result.to_json() == data


def test_domain_contact_organization_missing_should_throw():
    data = {
        "type": "org",
        "name": "Mr. Test",
        "street": ["DisneyLand"],
        "postalCode": "012345",
        "state": "BER",
        "country": "de",
        "city": "Aachen",
        "emailAddress": "me@example.com",
        "phoneNumber": "+1 1234 6859321",
    }

    with pytest.raises(ContextConditionException):
        DomainContact.from_json(data)


def test_domain_contact_organization_parsed():
    data = {
        "type": "org",
        "organization": "TestOrg",
        "name": "Mr. Test",
        "street": ["DisneyLand"],
        "postalCode": "012345",
        "state": "BER",
        "country": "de",
        "city": "Aachen",
        "emailAddress": "me@example.com",
        "phoneNumber": "+1 1234 6859321",
    }

    result = DomainContact.from_json(data)

    assert result.organization == "TestOrg"
