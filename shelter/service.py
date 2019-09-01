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
            pet = await self._pets_repo.add(data)
        except (KeyError, ValueError, TypeError) as e:
            print(e)
            raise web.HTTPBadRequest
        return web.json_response(pet.asdict(), status=201)

    async def pet_list(self, _):
        pets = await self._pets_repo.all()
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
            print(e)
            raise web.HTTPBadRequest
        return web.json_response(pet.asdict(), status=201)

    async def pet_delete(self, request):
        pet_id = int(request.match_info['pet_id'])
        await self._pets_repo.delete(pet_id)
        return web.HTTPSuccessful

    async def shelter_create(self, request):
        data = await request.json()
        try:
            shelter = await self._shelters_repo.add(data)
        except (KeyError, ValueError, TypeError) as e:
            print(e)
            raise web.HTTPBadRequest
        return web.json_response(shelter.asdict(), status=201)

    async def shelter_list(self, _):
        shelters = await self._shelters_repo.all()
        return web.json_response([
            shelter.asdict() for shelter in shelters
        ])

    async def shelter_retrieve(self, request):
        shelter_id = int(request.match_info['shelter_id'])
        shelter = await self._shelters_repo.get_by_id(shelter_id)
        if shelter:
            return web.json_response(shelter.asdict())
        raise web.HTTPNotFound
