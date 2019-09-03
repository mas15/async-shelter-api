from typing import Dict

from shelter.data import db
from shelter.data.base_repository import BaseGinoRepository
from shelter.entities.shelter_data_storage import ShelterDataStorage


class ShelterModel(db.Model):
    __tablename__ = 'shelters'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(255))
    fullAddress = db.Column(db.Unicode(255))
    city = db.Column(db.Unicode(255))
    petsAvailable = db.Column(db.Integer())

    def asdict(self):
        return {
            'id': self.id,
            'name': self.name,
            'fullAddress': self.fullAddress,
            'city': self.city,
            'petsAvailable': self.petsAvailable
        }


class PostgresSheltersRepository(ShelterDataStorage, BaseGinoRepository):
    async def add(self, shelter_data: Dict):
        async with self.transaction():
            p = await ShelterModel.create(**shelter_data)
            return p

    async def get_by_id(self, shelter_id: int):
        async with self.transaction():
            shelter = await ShelterModel.get(shelter_id)
            return shelter

    async def all(self, city=None):
        async with self.transaction():
            shelters_query = ShelterModel.query
            if city:
                shelters_query = shelters_query.where(ShelterModel.city == city)
            shelters = await shelters_query.gino.all()
            return shelters
