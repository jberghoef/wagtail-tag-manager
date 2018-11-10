.PHONY: install clean requirements test retest lint flake8 isort sandbox bundle watch git-reset

default: install

install: clean requirements bundle

clean:
	find src -name '*.pyc' -delete
	find tests -name '*.pyc' -delete
	find . -name '*.egg-info' |xargs rm -rf

requirements:
	pip install --upgrade -e .[docs,test]

test:
	py.test --nomigrations --reuse-db tests/

retest:
	py.test --nomigrations --reuse-db tests/ -vvv

coverage:
	py.test --nomigrations --reuse-db tests/ --cov=wagtail_tag_manager --cov-report=term-missing --cov-report=html

lint: flake8 isort

flake8:
	flake8 src/ tests/

isort:
	pip install isort
	isort --recursive src tests

format:
	pip install black
	black --py36 --verbose --exclude "/(\.git|\.hg|\.mypy_cache|\.tox|\.venv|_build|buck-out|build|dist|migrations)/" ./src
	black --py36 --verbose --exclude "/(\.git|\.hg|\.mypy_cache|\.tox|\.venv|_build|buck-out|build|dist|migrations)/" ./tests
	yarn install
	prettier --write ./frontend/**/*

sandbox: bundle
	pip install -r sandbox/requirements.txt
	sandbox/manage.py migrate
	sandbox/manage.py loaddata sandbox/exampledata/users.json
	sandbox/manage.py loaddata sandbox/exampledata/cms.json
	sandbox/manage.py loaddata sandbox/exampledata/wtm.json
	sandbox/manage.py runserver

bundle:
	yarn install --force
	yarn build

watch:
	yarn dev
	yarn watch

release:
	pip install twine wheel
	rm -rf dist/*
	python setup.py sdist bdist_wheel upload -r pypi
