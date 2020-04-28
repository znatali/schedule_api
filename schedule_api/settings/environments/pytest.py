# -*- coding: utf-8 -*-

"""Override any custom settings for pytest here."""
from schedule_api.settings.components.logging import LOGGING

DOCKER_IMG = 'pytest-mock-'
SECRET_KEY = '__CHANGEME__'
DB_TOOLS_URL_PREFIX = 'pt'

LOGGING['loggers']['django.db.backends'] = {'level': 'WARNING'}  # type: ignore
