import asyncio

import pytest
import requests

from shelter.data import db


@pytest.fixture()
def prepare_db():
    async def _prepare_db():
        await db.set_bind('postgresql://postgres@localhost:5432')
        await db.gino.drop_all()
        await db.gino.create_all()
    asyncio.run(_prepare_db())


@pytest.mark.usefixtures('prepare_db')
def test_all_at_once():
    response = requests.post('http://localhost:8080/shelters', json={
        'name': 'Schronisko Pod Lipą',
        'fullAddress': 'ul. Lipowa 18, 00-123 Będzin',
        'city': 'Będzin',
        'petsAvailable': 13
    })
    assert response.status_code == 201
    shelter_id = response.json()['id']

    response = requests.post('http://localhost:8080/pets', json={
        'name': 'Bürek',
        'type': 'dog',
        'available': True,
        'adoptedAt': None,
        'description': 'owczarek niemiecki, ładny piesek, nie ma pcheł',
        'shelterID': shelter_id
    })
    assert response.status_code == 201
    pet = response.json()
    pet_id = response.json()['id']

    response = requests.get(f'http://localhost:8080/pets/{pet_id}')
    assert response.status_code == 200
    assert response.json() == pet

    response = requests.post('http://localhost:8080/pets', json={
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

    response = requests.get(f'http://localhost:8080/pets')
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = requests.get(f'http://localhost:8080/pets?type=cat')
    assert response.status_code == 200
    assert response.json() == [cat]

    response = requests.get(f'http://localhost:8080/pets?type=dog')
    assert response.status_code == 200
    assert response.json() == [pet]

    response = requests.get(f'http://localhost:8080/pets?type=monkey')
    assert response.status_code == 404

    response = requests.delete(f'http://localhost:8080/pets/{pet_id}')
    assert response.status_code == 200

    response = requests.get(f'http://localhost:8080/pets/{pet_id}')
    assert response.status_code == 404