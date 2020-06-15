import logging.config
import os

# DB
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DB = os.getenv("PG_DB")

PG_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

# LOGS
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'console_formatter': {
            'format': '[%(asctime)s]:[%(process)d] | [%(levelname)s] | %(name)-15s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console_formatter'
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    }
}

logging.config.dictConfig(LOGGING)
