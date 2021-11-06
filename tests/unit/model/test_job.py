from hostingde.model.job import Job, JobStatus


def test_job_constructor():
    job: Job = Job(
        account_id='account',
        action='create',
        add_date='Timeslot',
        display_name="cloudfux.de",
        id="38426570vds125970v",
        last_change_date="Timeslot2",
        object_id="32957vwge715br",
        object_type="Zone",
        parent_job_id=None,
        status=JobStatus.successful
    )

    assert job.account_id == 'account'
    assert job.action == 'create'
    assert job.add_date == 'Timeslot'
    assert job.display_name == "cloudfux.de"
    assert job.id == "38426570vds125970v"
    assert job.last_change_date == "Timeslot2"
    assert job.object_id == "32957vwge715br"
    assert job.object_type == "Zone"
    assert job.parent_job_id is None
    assert job.status == JobStatus.successful


def test_job_to_str():
    job: Job = Job(
        account_id='account',
        action='create',
        add_date='Timeslot',
        display_name="cloudfux.de",
        id="38426570vds125970v",
        last_change_date="Timeslot2",
        object_id="32957vwge715br",
        object_type="Zone",
        parent_job_id=None,
        status=JobStatus.successful
    )

    assert str(job) == "cloudfux.de -> successful"


def test_parse_job_object():
    # TODO: Marshmallow bug with enum integration
    data = dict(
        accountId='account',
        action='create',
        addDate='Timeslot',
        displayName="cloudfux.de",
        id="38426570vds125970v",
        lastChangeDate="Timeslot2",
        objectId="32957vwge715br",
        objectType="Zone",
        parentJobId=None,
        status='successful'
    )

    job: Job = Job.from_json(data)

    assert job.account_id == 'account'
    assert job.action == 'create'
    assert job.add_date == 'Timeslot'
    assert job.display_name == "cloudfux.de"
    assert job.id == "38426570vds125970v"
    assert job.last_change_date == "Timeslot2"
    assert job.object_id == "32957vwge715br"
    assert job.object_type == "Zone"
    assert job.parent_job_id is None
    assert job.status == JobStatus.successful
