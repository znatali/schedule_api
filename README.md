# Simple Django Rest API for setup a university schedule and export to docs/xls - WORK IN PROGRESS
[![Build Status](https://travis-ci.org/znatali/schedule_api.svg?branch=master)](https://travis-ci.org/znatali/schedule_api)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Simple Django Rest API. Check out the project's [documentation](http://znatali.github.io/schedule_api/).


TODO for:
Environment:
1. Use [poetry](https://python-poetry.org/) for external packages. Remove usage of pip.
2. Update config of the project to use env template.

Project:
1. Validation of the Schedule, ScheduleDay, ScheduleItem.
2. Add version to models.
3. Implement teaching_subject model.
4. Add translation.
5. Export Schedule to doc.


# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

To add new package(s):
1.  Add to requirements.txt
2. Run 
```bash
docker-compose build
```

To run tests:
```bash
docker-compose run --rm web ./manage.py test
```