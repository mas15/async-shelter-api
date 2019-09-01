import dataclasses
from enum import Enum


class PetType(Enum):
    dog = 'dog'
    cat = 'cat'


@dataclasses.dataclass
class Pet:
    id: str
    name: str
    type: PetType
    available: bool
    addedAt: bool
    adoptedAt: bool
    description: str
    shelterID: str

    def asdict(self):
        return dataclasses.asdict(self)
