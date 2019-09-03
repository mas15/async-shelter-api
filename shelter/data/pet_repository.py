from typing import Dict

from shelter.data import db
from shelter.data.base_repository import BaseGinoRepository
from shelter.entities.pet_data_storage import PetDataStorage


class PetModel(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(255))
    type = db.Column(db.Unicode(255))
    available = db.Column(db.Boolean())
    addedAt = db.Column(db.DateTime())
    adoptedAt = db.Column(db.DateTime())
    description = db.Column(db.Unicode(255))
    shelterID = db.Column(db.Integer, db.ForeignKey('shelters.id'))

    def asdict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'available': self.available,
            'addedAt': str(self.addedAt) if self.addedAt else None,
            'adoptedAt': str(self.adoptedAt) if self.adoptedAt else None,
            'description': self.description,
            'shelterID': self.shelterID
        }


class PostgresPetsRepository(PetDataStorage, BaseGinoRepository):
    async def add(self, pet_data: Dict) -> PetModel:
        async with self.transaction():
            p = await PetModel.create(**pet_data)
            return p

    async def get_by_id(self, pet_id: int):
        async with self.transaction():
            pet = await PetModel.get(pet_id)
            return pet

    async def get_by_shelter(self, shelter_id: str):
        pets = await PetModel.query.where(PetModel.shelterID == shelter_id).gino.all()
        return pets

    async def all(self, pet_type=None, shelter_id=None):
        async with self.transaction():
            pets_query = PetModel.query
            if pet_type:
                pets_query = pets_query.where(PetModel.type == pet_type)
            if shelter_id:
                pets_query = pets_query.where(PetModel.shelterID == shelter_id)
            pets = await pets_query.gino.all()
            return pets

    async def update(self, pet_id: str, data: Dict):
        async with self.transaction():
            pet = await PetModel.get(pet_id)
            await pet.update(**data).apply()
            return pet

    async def delete(self, pet_id):
        async with self.transaction():
            await PetModel.delete.where(PetModel.id == pet_id).gino.status()
