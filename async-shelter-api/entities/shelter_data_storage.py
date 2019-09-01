import abc


class ShelterDataStorage(abc.ABC):
    @abc.abstractmethod
    async def add(self, shelter):
        pass

    @abc.abstractmethod
    async def get_by_id(self, shelter_id):
        pass

    @abc.abstractmethod
    async def all(self):
        pass

