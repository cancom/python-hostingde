from dataclasses import dataclass
from enum import Enum
from typing import Optional

from marshmallow_enum import EnumField

from hostingde.model import Model


class JobStatus(Enum):
    inProgress = 'inProgress'
    successful = 'successful'
    failed = 'failed'
    canceled = 'canceled'
    new = 'new'
    support = 'support'


@dataclass
class Job(Model):
    account_id: Optional[str]
    action: Optional[str]
    add_date: Optional[str]
    display_name: Optional[str]
    id: Optional[str]
    last_change_date: Optional[str]
    object_id: Optional[str]
    object_type: Optional[str]
    parent_job_id: Optional[str]
    status: Optional[JobStatus] = EnumField(JobStatus)

    def __init__(
        self,
        account_id: str = None,
        action: str = None,
        add_date: str = None,
        display_name: str = None,
        id: str = None,
        last_change_date: str = None,
        object_id: str = None,
        object_type: str = None,
        parent_job_id: str = None,
        status: JobStatus = None,
        **kwargs: dict,
    ) -> None:
        """
        Represents a job.

        :param account_id: The account id that this job belongs to.
        :param action: The action of the job, e.g. 'create', 'delete'
        :param add_date: When the job was first started.
        :param display_name: The readable name of the resource affected
        :param id: The unique job id.
        :param last_change_date: When the job was last updated.
        :param object_id: The id of the object affected by the job
        :param object_type: The type of the object, e.g. 'Zone', 'Record'
        :param parent_job_id: If the job was started by another job
        :param status: The current status of the job, e.g. 'inProgress', 'successfull'
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.account_id = account_id
        self.action = action
        self.add_date = add_date
        self.display_name = display_name
        self.id = id
        self.last_change_date = last_change_date
        self.object_id = object_id
        self.object_type = object_type
        self.parent_job_id = parent_job_id
        self.status = status

    def __str__(self):
        return f"{self.display_name} -> {self.status.value}"
