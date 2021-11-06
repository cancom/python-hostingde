from hostingde.model.record import Record, RecordType


def test_record_constructor():
    record = Record(
        id='234987fds',
        zone_id="wegsefgio345235",
        record_template_id="templateid",
        name="recordname",
        type=RecordType.A,
        last_change_date="some_timestamp",
        content="127.0.0.1",
        priority=0,
        ttl=0
    )

    assert record.id == '234987fds'

    assert record.id == '234987fds'
    assert record.zone_id == "wegsefgio345235"
    assert record.record_template_id == "templateid"
    assert record.name == "recordname"
    assert record.type == RecordType.A
    assert record.last_change_date == "some_timestamp"
    assert record.content == "127.0.0.1"
    assert record.priority == 0
    assert record.ttl == 0


def test_parse_record():
    data = dict(
        id='234987fds',
        zoneId="wegsefgio345235",
        recordTemplateId="templateid",
        name="recordname",
        type="A",
        lastChangeDate="some_timestamp",
        content="127.0.0.1",
        priority=0,
        ttl=0
    )

    record = Record.from_json(data)

    assert record.id == '234987fds'
    assert record.zone_id == "wegsefgio345235"
    assert record.record_template_id == "templateid"
    assert record.name == "recordname"
    assert record.type == RecordType.A
    assert record.last_change_date == "some_timestamp"
    assert record.content == "127.0.0.1"
    assert record.priority == 0
    assert record.ttl == 0


def test_dump_record():
    record = Record(
        id='234987fds',
        zone_id="wegsefgio345235",
        record_template_id="templateid",
        name="recordname",
        type=RecordType.A,
        last_change_date="some_timestamp",
        content="127.0.0.1",
        priority=0,
        ttl=0
    )

    assert record.to_json() == dict(
        id='234987fds',
        zoneId="wegsefgio345235",
        recordTemplateId="templateid",
        name="recordname",
        type="A",
        lastChangeDate="some_timestamp",
        content="127.0.0.1",
        priority=0,
        ttl=0
    )


def test_create_new_record():
    record = Record.create_new_record('cloud.de', RecordType.A, "127.0.0.1")

    assert record.name == "cloud.de"
    assert record.type == RecordType.A
    assert record.content == "127.0.0.1"

    assert record.ttl == 86400
    assert record.priority is None

    assert record.zone_id is None
    assert record.record_template_id is None
    assert record.last_change_date is None
