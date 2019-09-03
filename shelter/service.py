import logging
from datetime import datetime

from aiohttp import web
from shelter.entities.pet_data_storage import PetDataStorage
from shelter.entities.shelter_data_storage import ShelterDataStorage


class APIService:
    def __init__(self, pets_repo: PetDataStorage, shelters_repo: ShelterDataStorage):
        self._pets_repo = pets_repo
        self._shelters_repo = shelters_repo

    async def pet_create(self, request):
        data = await request.json()
        try:
            shelter_id = int(data['shelterID'])
            shelter = await self._shelters_repo.get_by_id(shelter_id)
            if not shelter:
                logging.info(f'Could not find shelter with id {shelter_id}')
                raise web.HTTPNotFound
            data['addedAt'] = datetime.now()
            pet = await self._pets_repo.add(data)
        except (KeyError, ValueError, TypeError) as e:
            logging.exception(e)
            raise web.HTTPBadRequest
        return web.json_response(pet.asdict(), status=201)

    async def pet_list(self, request):
        pet_type = request.rel_url.query.get('type')
        shelter_id = request.rel_url.query.get('shelter_id')
        pets = await self._pets_repo.all(pet_type=pet_type, shelter_id=shelter_id)
        if not pets:
            raise web.HTTPNotFound
        return web.json_response([
            pet.asdict() for pet in pets
        ])

    async def pet_retrieve(self, request):
        pet_id = int(request.match_info['pet_id'])
        pet = await self._pets_repo.get_by_id(pet_id)
        if pet:
            return web.json_response(pet.asdict())
        raise web.HTTPNotFound

    async def pet_update(self, request):
        data = await request.json()
        try:
            pet_id = data.pop('id')
            pet = await self._pets_repo.update(pet_id, data)
        except (KeyError, ValueError, TypeError) as e:
            logging.exception(e)
            raise web.HTTPBadRequest
        return web.json_response(pet.asdict(), status=201)

    async def pet_delete(self, request):
        pet_id = int(request.match_info['pet_id'])
        await self._pets_repo.delete(pet_id)
        logging.info(f'Deleted pet with id {pet_id}')
        return web.Response(status=200)

    async def shelter_create(self, request):
        data = await request.json()
        try:
            shelter = await self._shelters_repo.add(data)
        except (KeyError, ValueError, TypeError) as e:
            logging.exception(e)
            raise web.HTTPBadRequest
        return web.json_response(shelter.asdict(), status=201)

    async def shelter_list(self, request):
        city = request.rel_url.query.get('city')
        shelters = await self._shelters_repo.all(city=city)
        return web.json_response([
            shelter.asdict() for shelter in shelters
        ])

    async def shelter_retrieve(self, request):
        shelter_id = int(request.match_info['shelter_id'])
        shelter = await self._shelters_repo.get_by_id(shelter_id)
        if shelter:
            return web.json_response(shelter.asdict())
        raise web.HTTPNotFound

    async def shelter_retrieve_pets(self, request):
        shelter_id = int(request.match_info['shelter_id'])
        pet_type = request.rel_url.query.get('type')
        pets = await self._pets_repo.all(pet_type=pet_type, shelter_id=shelter_id)
        return web.json_response([
            pet.asdict() for pet in pets
        ])
