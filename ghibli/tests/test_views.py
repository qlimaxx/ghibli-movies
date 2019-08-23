import mock

from django.test import TestCase
from django.urls import reverse


MOVIES = [{
    'title': 'movie1',
    'people': [{'name': 'person1'}]
}]


class ViewsTest(TestCase):

    @mock.patch('django.core.cache.cache.get', return_value=MOVIES)
    def test_expected_movies_view(self, cache_get_func):
        response = self.client.get(reverse('ghibli:movies'))
        self.assertTrue(cache_get_func.called)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['movies'], MOVIES)
        self.assertTemplateUsed(response, 'ghibli/movies.html')
