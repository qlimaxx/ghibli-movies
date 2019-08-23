import mock

from django.test import TestCase
from django.conf import settings
from django.core.cache import cache

from ghibli.tasks import ghibli_fetch_movies


FILMS = [{
    'title': 'movie1',
    'people': [{'name': 'person1'}]
}]


class TasksTest(TestCase):

    @mock.patch('ghibli.tasks.fetch_movies_with_people', return_value=FILMS)
    def test_ghibli_fetch_movies_succeeded(self, fetch_movies_func):
        task = ghibli_fetch_movies.s().apply()
        result = cache.get(settings.GHIBLI_CACHE_KEY)
        self.assertTrue(fetch_movies_func.called)
        self.assertEqual(task.status, 'SUCCESS')
        self.assertEqual(result, FILMS)

    @mock.patch('ghibli.tasks.fetch_movies_with_people', return_value=[])
    def test_ghibli_fetch_movies_with_empty_films(self, fetch_movies_func):
        cache.set(settings.GHIBLI_CACHE_KEY, FILMS)
        task = ghibli_fetch_movies.s().apply()
        result = cache.get(settings.GHIBLI_CACHE_KEY)
        self.assertTrue(fetch_movies_func.called)
        self.assertEqual(task.status, 'SUCCESS')
        self.assertEqual(result, FILMS)

    def tearDown(self):
        cache.delete(settings.GHIBLI_CACHE_KEY)
