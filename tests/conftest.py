import arrow
import pytest
from freezegun import freeze_time

from shelter.service import APIService
from tests.ondisk_pets_repository import OnDiskPetsRepository
from tests.ondisk_shelter_repository import OnDiskSheltersRepository


@pytest.fixture(autouse=True)
def current_time():
    with freeze_time("2005-04-02 21:37:00"):
        yield arrow.now().naive


@pytest.fixture
def pets_repo():
    return OnDiskPetsRepository()


@pytest.fixture
def shelters_repo():
    return OnDiskSheltersRepository()


@pytest.fixture
def api_handler(pets_repo, shelters_repo):
    return APIService(pets_repo, shelters_repo)


@pytest.fixture()
def pet_data():
    return {
        'name': 'Burek',
        'type': 'dog',
        'available': True,
        'shelterID': '1',
        'description': 'description'
    }


@pytest.fixture()
def shelter_data():
    return {
        'name': 'shelter',
        'fullAddress': 'adress',
        'city': 'city',
        'petsAvailable': 11,
    }


@pytest.fixture()
async def pet(loop, pet_data, pets_repo, shelter, current_time):
    pet_data['addedAt'] = str(current_time)
    pet = await pets_repo.add(pet_data)
    return pet


@pytest.fixture()
async def shelter(loop, shelter_data, shelters_repo):
    shelter = await shelters_repo.add(shelter_data)
    return shelter
