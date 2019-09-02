import requests

if __name__ == '__main__':
    response = requests.post('http://localhost:8080/shelters', json={
        # 'id': 'bd09b2f0-c274-11e9-963b-6b7b4dc28ba0', todo
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
        'addedAt': '2019-08-19 12:31:12',
        'adoptedAt': None,
        'description': 'owczarek niemiecki, ładny piesek, nie ma pcheł',
        'shelterID': str(shelter_id)
    })
    assert response.status_code == 201
    pet_id = response.json()['id']

    response = requests.get(f'http://localhost:8080/pets/{pet_id}')
    assert response.status_code == 200

    response = requests.delete(f'http://localhost:8080/pets/{pet_id}')
    assert response.status_code == 200

    response = requests.get(f'http://localhost:8080/pets/{pet_id}')
    assert response.status_code == 404
