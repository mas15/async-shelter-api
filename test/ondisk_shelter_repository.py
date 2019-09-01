from shelter.entities.shelter_data_storage import ShelterDataStorage


class OnDiskSheltersRepository(ShelterDataStorage):
    def __init__(self):
        self.shelters = dict()

    async def add(self, shelter):
        self.shelters[shelter.id] = shelter

    async def get_by_id(self, shelter_id):
        return self.shelters[shelter_id]

    async def all(self):
        return self.shelters.values()
