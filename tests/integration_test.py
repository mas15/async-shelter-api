import asyncio

import pytest
import requests

from shelter.data import db

URL_HOST = 'http://localhost:8080'


@pytest.fixture()
def prepare_db():
    async def _prepare_db():
        await db.set_bind('postgresql://postgres@localhost:5432')
        await db.gino.drop_all()
        await db.gino.create_all()
    asyncio.run(_prepare_db())


@pytest.fixture()
def shelter_id():
    response = requests.post(f'{URL_HOST}/shelters', json={
        'name': 'Schronisko Pod Lipą',
        'fullAddress': 'ul. Lipowa 18, 00-123 Będzin',
        'city': 'Będzin',
        'petsAvailable': 13
    })
    assert response.status_code == 201
    return response.json()['id']


@pytest.fixture()
def dog(shelter_id):
    response = requests.post(f'{URL_HOST}/pets', json={
        'name': 'Bürek',
        'type': 'dog',
        'available': True,
        'adoptedAt': None,
        'description': 'owczarek niemiecki, ładny piesek, nie ma pcheł',
        'shelterID': shelter_id
    })
    assert response.status_code == 201
    return response.json()


@pytest.mark.usefixtures('prepare_db')
def test_all_pet_get_endpoints(shelter_id, dog):
    response = requests.get(f'{URL_HOST}/pets/{dog["id"]}')
    assert response.status_code == 200
    assert response.json() == dog

    response = requests.post(f'{URL_HOST}/pets', json={
        'name': 'Kotek',
        'type': 'cat',
        'available': False,
        'adoptedAt': None,
        'description': 'kotek',
        'shelterID': shelter_id
    })
    assert response.status_code == 201
    cat = response.json()
    cat_id = response.json()['id']

    response = requests.get(f'{URL_HOST}/pets')
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = requests.get(f'{URL_HOST}/pets?type=cat')
    assert response.status_code == 200
    assert response.json() == [cat]

    response = requests.get(f'{URL_HOST}/pets?type=dog')
    assert response.status_code == 200
    assert response.json() == [dog]

    response = requests.get(f'{URL_HOST}/pets?type=monkey')
    assert response.status_code == 404

    response = requests.get(f'{URL_HOST}/shelters/{shelter_id}/pets')
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = requests.get(f'{URL_HOST}/shelters/{shelter_id}/pets?type=dog')
    assert response.status_code == 200
    assert response.json() == [dog]


@pytest.mark.usefixtures('prepare_db')
def test_all_pet_delete(dog):
    response = requests.delete(f'{URL_HOST}/pets/{dog["id"]}')
    assert response.status_code == 200

    response = requests.get(f'{URL_HOST}/pets/{dog["id"]}')
    assert response.status_code == 404


@pytest.mark.usefixtures('prepare_db')
def test_all_shelter_endpoints_once():
    response = requests.post(f'{URL_HOST}/shelters', json={
        'name': 'Schronisko Pod Lipą',
        'fullAddress': 'ul. Lipowa 18, 00-123 Będzin',
        'city': 'Będzin',
        'petsAvailable': 13
    })
    assert response.status_code == 201

    response = requests.post(f'{URL_HOST}/shelters', json={
        'name': 'Schronisko Drugie',
        'fullAddress': 'ul. Lipowa 18, 00-123 Będzin',
        'city': 'Warszawa',
        'petsAvailable': 50
    })
    assert response.status_code == 201
    shelter2 = response.json()

    response = requests.get(f'{URL_HOST}/shelters')
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = requests.get(f'{URL_HOST}/shelters?city=Warszawa')
    assert response.status_code == 200
    assert response.json() == [shelter2]

