# -*- coding: utf-8 -*-

# Logging
# https://docs.djangoproject.com/en/2.2/topics/logging/

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s [%(module)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'axes': {
            'handlers': ['console'],
            'level': 'WARN',
        },
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
