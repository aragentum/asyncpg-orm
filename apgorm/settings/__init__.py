import logging
import os
from os import path

BASE_PATH = path.dirname(path.dirname(path.abspath(__file__)))
ROOT_PATH = path.abspath(path.join(BASE_PATH, '..'))

ENV_FILE = path.join(ROOT_PATH, '.env')

# set environment variables
if path.exists(ENV_FILE):
    logger = logging.getLogger(__name__)
    with open(ENV_FILE, 'r') as file:
        env_vars = file.readlines()
    for env_var in env_vars:
        if not env_var:
            continue
        env_var = env_var.strip()
        key, value = env_var.split('=')
        if not key or not isinstance(key, str) or not value:
            continue
        os.environ[key] = value
        logger.info(f'Set env {key}')

from .base import *
