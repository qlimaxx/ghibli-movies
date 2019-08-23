from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.cache import cache
from celery.signals import worker_ready
from celery.utils.log import get_task_logger

from projconf.celery import app
from ghibli.utils.ghibli import fetch_movies_with_people


logger = get_task_logger(__name__)


@worker_ready.connect
@app.task
def ghibli_fetch_movies(**kwargs):
    logger.info('Starting fetching data from API')
    movies = fetch_movies_with_people()
    if movies:
        logger.info('Saving data from API')
        cache.set(settings.GHIBLI_CACHE_KEY, movies, timeout=None)
    logger.info('Fetching data succeeded')
