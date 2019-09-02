import abc
from typing import Dict


class PetDataStorage(abc.ABC):
    @abc.abstractmethod
    async def add(self, pet_data: Dict):
        pass

    @abc.abstractmethod
    async def get_by_id(self, pet_id):
        pass

    @abc.abstractmethod
    async def get_by_shelter(self, shelter_id):
        pass

    @abc.abstractmethod
    async def all(self, pet_type=None, shelter_id=None):
        pass

    @abc.abstractmethod
    async def update(self, pet_id, data):
        pass

    @abc.abstractmethod
    async def delete(self, pet_id):
        pass
