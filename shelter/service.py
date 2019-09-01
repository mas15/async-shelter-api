import logging
import uuid

from aiohttp import web

from shelter.entities.pet import Pet


class APIService:
    def __init__(self, database):
        self._database = database

    async def pet_list(self, _):
        pets = await self._database.all_pets()
        return web.json_response([
            pet.asdict() for pet in pets
        ])

    async def pet_create(self, request):
        request_data = await request.json()
        pet_id = str(uuid.uuid4())
        try:
            pet = Pet(
                id=pet_id
            )
        except (KeyError, ValueError, TypeError):
            raise web.HTTPBadRequest
        await self._database.add_pet(pet)
        return web.json_response(pet.asdict(), status=201)

    async def pet_retrieve(self, request):
        pet_id = request.match_info['pet_id']
        pet = await self._database.get_pet(pet_id)
        if pet:
            return web.json_response(pet.asdict())
        raise web.HTTPNotFound

    async def pet_update(self, request):
        # TODO
        pass

    async def pet_delete(self, request):
        pet_id = request.match_info['pet_id']
        await self._database.remove_pet(pet_id)
        return web.HTTPSuccessful


async def make_app():
    app = web.Application()
    database = PostgresDB.create()
    handler = APIService(database)
    app.add_routes([
        web.get('/pets', handler.pet_list),
        web.post('/pets', handler.pet_create),
        web.patch('/pets', handler.pet_update),
        web.delete('/pets', handler.pet_delete),
        web.get('/pets/{pet_id}', handler.pet_retrieve),

        web.get('/shelters', handler.shelter_list),
        web.post('/shelters', handler.shelter_create),
        web.get('/shelters/{shelter_id}', handler.shelter_retrieve),
        web.get('/shelters/{shelter_id}/pets', handler.shelter_retrieve_pets)
    ])
    return app


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    web.run_app(make_app())
