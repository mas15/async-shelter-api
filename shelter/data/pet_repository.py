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
    addedAt = db.Column(db.Unicode(255)) # db.DateTime()
    adoptedAt = db.Column(db.Unicode(255)) # db.DateTime()
    description = db.Column(db.Unicode(255))
    shelterID = db.Column(db.Unicode(255))
    # shelterID = db.Column(None, db.ForeignKey('shelters.id'))

    def asdict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'available': self.available,
            'addedAt': self.addedAt,
            'adoptedAt': self.adoptedAt,
            'description': self.description,
            'shelterID': self.shelterID
        }


class PostgresPetsRepository(PetDataStorage, BaseGinoRepository):
    async def add(self, pet_data: Dict):
        async with self.transaction():
            p = await PetModel.create(**pet_data)
            return p

    async def get_by_id(self, pet_id: int):
        async with self.transaction():
            pet = await PetModel.get(pet_id)
            return pet

    async def get_by_shelter(self, shelter_id):
        pets = await PetModel.query.where(PetModel.shelterID == shelter_id).gino.all()
        return pets

    async def all(self, pet_type=None, shelter_id=None):
        async with self.transaction():
            pets = await PetModel.query.gino.all()
            return pets

    async def update(self, pet_id, data):
        async with self.transaction():
            pet = await PetModel.get(pet_id)
            pet.update(**data).apply()
            return pet

    async def delete(self, pet_id):
        async with self.transaction():
            await PetModel.delete.where(PetModel.id == pet_id)
