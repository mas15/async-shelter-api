import dataclasses


@dataclasses.dataclass
class Shelter:
    id: str
    name: str
    fullAddress: str
    city: str
    petsAvailable: int

    def asdict(self):
        return dataclasses.asdict(self)
