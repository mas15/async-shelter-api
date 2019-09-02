from typing import Dict

from shelter.data.shelter_repository import ShelterModel
from shelter.entities.shelter_data_storage import ShelterDataStorage


class OnDiskSheltersRepository(ShelterDataStorage):
    def __init__(self):
        self.shelters = []
        self.id = 0

    async def add(self, shelter_data: Dict) -> ShelterModel:
        self.id += 1
        shelter = ShelterModel(id=self.id, **shelter_data)
        self.shelters.append(shelter)
        return shelter

    async def get_by_id(self, shelter_id):
        for shelter in self.shelters:
            if shelter.id == shelter_id:
                return shelter

    async def all(self, city=None):
        return self.shelters
