# Schedule Api

# Simple Django Rest API for setup a university schedule and export it to docs/xls - WORK IN PROGRESS

This project was generated with [`wemake-django-template`](https://github.com/wemake-services/wemake-django-template). Current template version is: [770bbf1e0dd96ca898ab50768b66b67e0cc8f78f](https://github.com/wemake-services/wemake-django-template/tree/770bbf1e0dd96ca898ab50768b66b67e0cc8f78f). See what is [updated](https://github.com/wemake-services/wemake-django-template/compare/770bbf1e0dd96ca898ab50768b66b67e0cc8f78f...master) since then.


[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services) 
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)


## Prerequisites

You will need:

- `python3.7` (see `pyproject.toml` for full version)
- `postgresql` with version `9.6`
- `docker` with [version at least](https://docs.docker.com/compose/compose-file/#compose-and-docker-compatibility-matrix) `18.02`


## Development

When developing locally, we use:

- [`editorconfig`](http://editorconfig.org/) plugin (**required**)
- [`poetry`](https://github.com/python-poetry/poetry) (**required**)
- `pycharm 2017+` or `vscode`


## Documentation

Full documentation is available here: [`docs/`](docs).



## Quick start with docker
~~~~~~~~~~~~~~
poetry shell
poetry install
docker-compose build
docker-compose run --rm web python manage.py migrate
docker-compose run --rm web ./manage.py createsuperuser --email super-admin@example.com --username super-admin
docker-compose up
~~~~~~~~~~~~~~

## Quick start for local development
~~~~~~~~~~~~~~
poetry shell
poetry install
psql postgres -U postgres -f sql/create_database.sql
python manage.py migrate
python manage.py runserver
~~~~~~~~~~~~~~


## Project TODO:
1. Add translation.
2. Advanced Export Schedule to docx.
