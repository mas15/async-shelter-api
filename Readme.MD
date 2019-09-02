## How to run it
```{bash}
make build
make run
```
API is running on port 8080 so that you can hit for example `http://localhost:8080/pets`

## How to run tests
```{bash}
make test
```


>>> requests.post('http://localhost:8080/pets', json={'name': 'aa', 'type': 'dog', 'available': True, 'shelterID': '111', 'adoptedAt': 'aa', 'addedAt': 'added', 'description': 'sas'})
>>> requests.post('http://localhost:8080/pets', json={'name': 'aa', 'type': 'dog', 'available': True, 'shelterID': '111', 'adoptedAt': 'aa', 'addedAt': 'added', 'description': 'sas'})
requests.post('http://localhost:8080/shelters', json={'name': 'shelter','fullAddress' : 'adress', 'city' : 'city',  'petsAvailable' : 11})

requests.get('http://localhost:8080/shelters')