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

I wrote also some very simple integration tests that can be used by
```{bash}
make docker_test
```


## Endpoints
```
GET /pets (?type=dog, ?shelterId=1)
GET /pets/<id>
POST /pets
PATCH /pets
DELETE /pets/<id>
GET /shelters (?city=warszawa)
GET /shelters/<id>
GET /shelters/<id>/pets (?type=dog)
POST /shelters
```