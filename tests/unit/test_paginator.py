import json

import responses

from hostingde.api import login
from hostingde.model.record import Record, RecordType
from hostingde.paginator import HostingDePaginator


@responses.activate
def test_paginator():
    api = login('https://example.de/api', 'token')

    url = 'https://example.de/api/demo'

    paginator: HostingDePaginator = HostingDePaginator(api, instance_class=Record, url=url)

    responses.add('POST', url, body=json.dumps({
        "response": {
            "data": [
                Record.create_new_record('cloud.de', RecordType.A, f'127.0.0.{i}').to_json() for i in range(25)
            ],
            "totalPages": 1
        },
        "status": "success"
    }))

    count = 0
    for item in paginator:
        assert item.content == f'127.0.0.{count}'
        count += 1

    assert count == 25


@responses.activate
def test_paginator_count_limited():
    api = login('https://example.de/api', 'token')

    url = 'https://example.de/api/demo'

    paginator: HostingDePaginator = HostingDePaginator(api, instance_class=Record, url=url, count=3)

    responses.add('POST', url, body=json.dumps({
        "response": {
            "data": [
                Record.create_new_record('cloud.de', RecordType.A, f'127.0.0.{i}').to_json() for i in range(25)
            ],
            "totalPages": 1
        },
        "status": "success"
    }))

    count = 0
    for item in paginator:
        assert item.content == f'127.0.0.{count}'
        count += 1

    assert count == 3


@responses.activate
def test_paginator_no_more_data():
    api = login('https://example.de/api', 'token')

    url = 'https://example.de/api/demo'

    paginator: HostingDePaginator = HostingDePaginator(api, instance_class=Record, url=url)

    responses.add('POST', url, body=json.dumps({
        "response": {
            "data": [
                Record.create_new_record('cloud.de', RecordType.A, f'127.0.0.{i}').to_json() for i in range(23)
            ],
            "totalPages": 2
        },
        "status": "success"
    }))

    responses.add('POST', url, body=json.dumps({
        "response": {
            "data": [
            ],
            "totalPages": 2
        },
        "status": "success"
    }))

    count = 0
    for item in paginator:
        assert item.content == f'127.0.0.{count}'
        count += 1

    assert count == 23


@responses.activate
def test_paginator_multipage():
    api = login('https://example.de/api', 'token')

    url = 'https://example.de/api/demo'

    paginator: HostingDePaginator = HostingDePaginator(api, instance_class=Record, url=url)

    responses.add('POST', url, body=json.dumps({
        "response": {
            "data": [
                Record.create_new_record('cloud.de', RecordType.A, f'127.0.0.{i}').to_json() for i in range(25)
            ],
            "totalPages": 2
        },
        "status": "success"
    }))

    responses.add('POST', url, body=json.dumps({
        "response": {
            "data": [
                Record.create_new_record('cloud.de', RecordType.A, f'127.0.0.{i}').to_json() for i in range(25, 41)
            ],
            "totalPages": 2
        },
        "status": "success"
    }))

    count = 0
    for item in paginator:
        print(count)
        assert item.content == f'127.0.0.{count}'
        count += 1

    assert count == 41


@responses.activate
def test_fetchall():
    api = login('https://example.de/api', 'token')

    url = 'https://example.de/api/demo'

    paginator: HostingDePaginator = HostingDePaginator(api, instance_class=Record, url=url)

    responses.add('POST', url, body=json.dumps({
        "response": {
            "data": [
                Record.create_new_record('cloud.de', RecordType.A, f'127.0.0.{i}').to_json() for i in range(25)
            ],
            "totalPages": 2
        },
        "status": "success"
    }))

    responses.add('POST', url, body=json.dumps({
        "response": {
            "data": [
                Record.create_new_record('cloud.de', RecordType.A, f'127.0.0.{i}').to_json() for i in range(25, 41)
            ],
            "totalPages": 2
        },
        "status": "success"
    }))

    assert len(paginator.fetchall()) == 41


@responses.activate
def test_fetchone():
    api = login('https://example.de/api', 'token')

    url = 'https://example.de/api/demo'

    paginator: HostingDePaginator = HostingDePaginator(api, instance_class=Record, url=url)

    responses.add('POST', url, body=json.dumps({
        "response": {
            "data": [
                Record.create_new_record('cloud.de', RecordType.A, f'127.0.0.{i}').to_json() for i in range(25)
            ],
            "totalPages": 2
        },
        "status": "success"
    }))

    responses.add('POST', url, body=json.dumps({
        "response": {
            "data": [
                Record.create_new_record('cloud.de', RecordType.A, f'127.0.0.{i}').to_json() for i in range(25, 41)
            ],
            "totalPages": 2
        },
        "status": "success"
    }))

    assert paginator.fetchone().content == '127.0.0.0'
