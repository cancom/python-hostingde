from dataclasses import dataclass

from hostingde.model import Model
from hostingde.model.domain import Domain


@dataclass
class RegisterDomainRequest(Model):
    domain: Domain
