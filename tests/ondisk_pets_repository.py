from typing import Dict

from shelter.data.pet_repository import PetModel
from shelter.entities.pet_data_storage import PetDataStorage


class OnDiskPetsRepository(PetDataStorage):
    def __init__(self):
        self.pets = []
        self.id = 0

    async def add(self, pet_data: Dict) -> PetModel:
        self.id += 1
        pet = PetModel(id=self.id, **pet_data)
        self.pets.append(pet)
        return pet

    async def get_by_id(self, pet_id):
        for pet in self.pets:
            if pet.id == pet_id:
                return pet

    async def get_by_shelter(self, pet_id):
        for pet in self.pets:
            if pet.id == pet_id:
                return pet

    async def all(self, pet_type=None, shelter_id=None):
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
        return pet
