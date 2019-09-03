.PHONY: run build test clean

run:
	docker-compose up

test: venv
	. venv/bin/activate && py.test tests/test_service.py -v

docker_test: venv
	. venv/bin/activate &&  docker-compose up -d && py.test tests/integration_test.py

coverage:
	py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=requests tests

venv:
	python3.7 -m venv venv; \
	. venv/bin/activate; \
	pip3 install -U pip; \
	pip3 install -e . ; \
	pip3 install -r tests/requirements.txt; \
	touch venv

clean:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info
	find . -name "*.pyc" -exec rm -f {} \;
	rm -rf venv

build:
	docker build -t shelter .
