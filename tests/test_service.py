import json

import pytest
from mock import Mock


@pytest.fixture()
def create_request(pet_data):
    async def json_data():
        return pet_data

    return Mock(json=json_data)


@pytest.fixture()
def update_request():
    async def json_data():
        return {'id': 1, 'name': 'Reksio'}

    return Mock(json=json_data)


@pytest.fixture()
def empty_request():
    async def json_data():
        return {}

    return Mock(json=json_data)


@pytest.mark.usefixtures('shelter')
@pytest.mark.asyncio
async def test_pet_create(api_handler, create_request, pets_repo):
    response = await api_handler.pet_create(create_request)
    pet_data = json.loads(response.text)
    assert response.status == 201
    pet = pets_repo.pets[0]
    assert pet_data == pet.asdict()


@pytest.mark.asyncio
async def test_pet_list(api_handler, pet, empty_request):
    response = await api_handler.pet_list(empty_request)
    data = json.loads(response.text)
    assert response.status == 200
    assert isinstance(data, list)
    assert data[0] == pet.asdict()


@pytest.mark.asyncio
async def test_pet_retrieve(api_handler, pet):
    get_request = Mock(match_info={'pet_id': '1'})
    response = await api_handler.pet_retrieve(get_request)
    pet_data = json.loads(response.text)
    assert response.status == 200
    assert pet_data == pet.asdict()


@pytest.mark.usefixtures('pet')
@pytest.mark.asyncio
async def test_pet_update(api_handler, update_request, current_time):
    response = await api_handler.pet_update(update_request)
    assert response.status

    get_request = Mock(match_info={'pet_id': '1'})
    response = await api_handler.pet_retrieve(get_request)
    pet_data = json.loads(response.text)
    assert response.status == 200
    assert pet_data == {
        'id': 1,
        'name': 'Reksio',
        'type': 'dog',
        'available': True,
        'addedAt': str(current_time),
        'adoptedAt': None,
        'description': 'description',
        'shelterID': '1'
    }
