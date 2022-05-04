.PHONY: install clean requirements test retest lint flake8 isort sandbox bundle watch git-reset

default: install

install: clean requirements bundle

clean:
	find src -name '*.pyc' -delete
	find tests -name '*.pyc' -delete
	find . -name '*.egg-info' |xargs rm -rf

requirements:
	yarn install
	pip install -U -e .[docs,test]

test:
	py.test --nomigrations --reuse-db tests/

retest:
	py.test --nomigrations --reuse-db tests/ -vvv

coverage:
	py.test --nomigrations --reuse-db tests/ --cov=wagtail_tag_manager --cov-report=term-missing --cov-report=html

lint: flake8 isort mypy

mypy:
	pip install -U mypy
	mypy src/ tests/

flake8:
	pip install -U flake8
	flake8 src/ tests/

isort:
	pip install -U isort
	isort --recursive src tests

format: black prettier

BLACK_EXCLUDE="/(\.git|\.hg|\.mypy_cache|\.tox|\.venv|_build|buck-out|build|dist|migrations)/"

black: isort
	pip install -U black
	black --target-version py37 --verbose --exclude $(BLACK_EXCLUDE) ./src
	black --target-version py37 --verbose --exclude $(BLACK_EXCLUDE) ./tests

prettier:
	yarn install
	yarn format

sandbox: bundle
	pip install -U -r sandbox/requirements.txt
	rm -rf db.sqlite3
	sandbox/manage.py migrate
	sandbox/manage.py loaddata sandbox/exampledata/users.json
	sandbox/manage.py loaddata sandbox/exampledata/cms.json
	sandbox/manage.py loaddata sandbox/exampledata/default_tags.json
	sandbox/manage.py loaddata sandbox/exampledata/additional_tags.json
	sandbox/manage.py runserver

test_sandbox:
	pip install -U -r sandbox/requirements.txt
	rm -rf db.sqlite3
	sandbox/manage.py migrate
	sandbox/manage.py loaddata sandbox/exampledata/users.json
	sandbox/manage.py loaddata sandbox/exampledata/cms.json
	sandbox/manage.py loaddata sandbox/exampledata/default_tags.json
	ENVIRONMENT=test sandbox/manage.py runserver --verbosity 0

bundle: prettier
	yarn install --force
	yarn build

watch:
	yarn dev
	yarn watch

release:
	pip install -U twine wheel
	rm -rf build/*
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine upload --repository pypi dist/*
