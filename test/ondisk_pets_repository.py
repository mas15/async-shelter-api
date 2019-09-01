from shelter.entities.pet_data_storage import PetDataStorage


class OnDiskPetsRepository(PetDataStorage):
    def __init__(self):
        self.pets = []

    async def add(self, pet):
        self.pets.append(pet)

    async def get_by_id(self, pet_id):
        for pet in self.pets:
            if pet.id == pet_id:
                return pet

    async def get_by_shelter(self, pet_id):
        for pet in self.pets:
            if pet.id == pet_id:
                return pet

    async def all(self):
        return self.pets

    async def delete(self, pet_id):
        pet = await self.get_by_id(pet_id)
        if pet:
            self.pets.remove(pet)

    async def update(self, pet_id, data):
        pet = await self.get_by_id(pet_id)
        if pet:
            for k, v in data.items():
                setattr(pet, k, v)
