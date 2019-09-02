import logging

from aiohttp import web

from shelter.data.pet_repository import PostgresPetsRepository
from shelter.data.shelter_repository import PostgresSheltersRepository
from shelter.service import APIService
from shelter.data import db


async def make_app():
    logging.info('STARTING....')
    app = web.Application()

    gino_engine = await db.set_bind('postgresql://postgres@postgres:5432')
    await db.gino.create_all()
    pets_repo = PostgresPetsRepository(gino_engine)
    shelters_repo = PostgresSheltersRepository(gino_engine)
    logging.info('DB STARTED.....')
    handler = APIService(pets_repo, shelters_repo)
    app.add_routes([
        web.get('/pets', handler.pet_list),
        web.post('/pets', handler.pet_create),
        web.patch('/pets', handler.pet_update),
        web.delete('/pets/{pet_id}', handler.pet_delete),
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
