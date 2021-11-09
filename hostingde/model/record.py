from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from marshmallow_enum import EnumField

from hostingde.model import Model


class RecordType(Enum):
    """
    Available relations for conditional filters.
    """

    A = 'A'
    AAAA = 'AAAA'
    ALIAS = 'ALIAS'
    CAA = 'CAA'
    CERT = 'CERT'
    CNAME = 'CNAME'
    DNSKEY = 'DNSKEY'
    DS = 'DS'
    MX = 'MX'
    NS = 'NS'
    NSEC = 'NSEC'
    NSEC3 = 'NSEC3'
    NSEC3PARAM = 'NSEC3PARAM'
    NULLMX = 'NULLMX'
    OPENPGPKEY = 'OPENPGPKEY'
    PTR = 'PTR'
    RRSIG = 'RRSIG'
    SRV = 'SRV'
    SOA = 'SOA'
    SSHFP = 'SSHFP'
    TLSA = 'TLSA'
    TXT = 'TXT'


@dataclass
class Record(Model):
    """The DNS Record object is part of a zone. It is used to manage DNS resource records."""

    id: Optional[str]
    zone_id: Optional[str]
    record_template_id: Optional[str]
    name: Optional[str]
    content: Optional[str]
    ttl: Optional[int]
    priority: Optional[int]
    last_change_date: Optional[str]
    type: Optional[RecordType] = EnumField(RecordType)

    def __init__(
        self,
        id: Optional[str] = None,
        zone_id: Optional[str] = None,
        record_template_id: Optional[str] = None,
        name: Optional[str] = None,
        type: Optional[RecordType] = None,
        content: Optional[str] = None,
        ttl: Optional[int] = None,
        priority: Optional[int] = None,
        last_change_date: Optional[str] = None,
        **kwargs: Any,
    ):
        """
        The DNS Record object is part of a zone. It is used to manage DNS resource records.

        :param id:                 Record ID. Ignored in create zone requzone_config.pyests. Either id or zoneId, name,
                                   type, and content are required in all other requests.

        :param zone_id:            ID of zone that the record belongs to.

        :param record_template_id: ID of record template the record is tied to. If empty, record has to be managed
                                   manually. If tied to record template, record will be removed or updated whenever
                                   record template is removed or updated.

        :param name:               Name of the record. Example: mail.example.com. Always required in create requests and
                                   in all other requests if no id is provided.

        :param type:
                                   Type of the record. Valid types are A, AAAA, ALIAS, CAA, CERT, CNAME, DNSKEY, DS, MX,
                                   NS, NSEC, NSEC3, NSEC3PARAM, NULLMX, OPENPGPKEY, PTR, RRSIG, SRV, SSHFP, TLSA, and
                                   TXT. Always required in create requests and in all other requests if no id is
                                   provided.

        :param content:            Content of the record. Always required in create requests and in all other requests
                                   if no id is provided.

        :param ttl:                TTL of the record in seconds. Minimum value: 60. Maximum value: 31556926 (one year).
                                   Exceeding the maximum or undercutting the minimum value will abort the request and
                                   result in an error.

        :param priority:           Priority of record. Only relevant if type is MX or SRV. Must be positive.

        :param last_change_date:   Date and time of last record modification
        """
        super().__init__(**kwargs)
        self.id = id
        self.zone_id = zone_id
        self.record_template_id = record_template_id
        self.name = name
        self.type = type
        self.content = content
        self.ttl = ttl
        self.priority = priority
        self.last_change_date = last_change_date

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Record):
            return False

        return self.name == other.name and self.type == other.type and self.content == other.content

    def __hash__(self) -> int:
        return hash(f'Name:{self.name}Type:{self.type.value if self.type else "No type"}Content:{self.content}')

    def __str__(self):
        return f"{self.name} {self.type.value} {self.content}"

    @staticmethod
    def create_new_record(
        name: str, type: RecordType, content: str, ttl: Optional[int] = 86400, priority: Optional[int] = None
    ) -> 'Record':
        return Record(name=name, type=type, content=content, ttl=ttl, priority=priority)
