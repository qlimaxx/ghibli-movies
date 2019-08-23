import requests
import requests_mock

from django.test import TestCase
from ghibli.utils import ghibli


FILMS = [{
    'id': 1,
    'title': 'movie1',
    'people': ['{}/1'.format(ghibli.PEOPLE_URL)]
}]

FILMS2 = [{
    'id': 1,
    'title': 'movie1',
    'people': ['{}/'.format(ghibli.PEOPLE_URL)]
}]

PEOPLE = [{
    'id': 1,
    'name': 'person1',
    'films': ['{}/1'.format(ghibli.FILMS_URL)]
}]

PERSON1 = PEOPLE[0]


class UtilsTest(TestCase):

    @requests_mock.Mocker()
    def test_fetch_movies_with_people_expected_result(self, m):
        m.get(ghibli.FILMS_URL, json=FILMS)
        m.get('{}/1'.format(ghibli.PEOPLE_URL), json=PERSON1)
        result = ghibli.fetch_movies_with_people()
        expected_result = [{
            'id': 1,
            'title': 'movie1',
            'people': [PERSON1]
        }]
        self.assertEqual(result, expected_result)

    @requests_mock.Mocker()
    def test_fetch_movies_with_people_not_ok_status_code_when_get_films(
            self,
            m):
        m.get(ghibli.FILMS_URL, status_code=404)
        result = ghibli.fetch_movies_with_people()
        self.assertEqual(result, [])

    @requests_mock.Mocker()
    def test_fetch_movies_with_people_not_ok_status_code_when_get_people(
            self,
            m):
        m.get(ghibli.FILMS_URL, json=FILMS2)
        m.get(ghibli.PEOPLE_URL, status_code=404)
        result = ghibli.fetch_movies_with_people()
        self.assertEqual(result, [])

    @requests_mock.Mocker()
    def test_fetch_movies_with_people_not_ok_status_code_when_get_person(
            self,
            m):
        m.get(ghibli.FILMS_URL, json=FILMS)
        m.get('{}/1'.format(ghibli.PEOPLE_URL), status_code=404)
        result = ghibli.fetch_movies_with_people()
        self.assertEqual(result, [])

    @requests_mock.Mocker()
    def test_fetch_movies_with_people_when_people_without_id(self, m):
        m.get(ghibli.FILMS_URL, json=FILMS2)
        m.get(ghibli.PEOPLE_URL, json=PEOPLE)
        result = ghibli.fetch_movies_with_people()
        expected_result = [{
            'id': 1,
            'title': 'movie1',
            'people': [PERSON1]
        }]
        self.assertEqual(result, expected_result)

    @requests_mock.Mocker()
    def test_fetch_movies_with_people_timeout_when_get_films(self, m):
        m.get(ghibli.FILMS_URL, exc=requests.exceptions.Timeout)
        result = ghibli.fetch_movies_with_people()
        self.assertEqual(result, [])

    @requests_mock.Mocker()
    def test_fetch_movies_with_people_timeout_when_get_get_people(self, m):
        m.get(ghibli.FILMS_URL, json=FILMS2)
        m.get(ghibli.PEOPLE_URL, exc=requests.exceptions.Timeout)
        result = ghibli.fetch_movies_with_people()
        self.assertEqual(result, [])

    @requests_mock.Mocker()
    def test_fetch_movies_with_people_timeout_when_get_get_person(self, m):
        m.get(ghibli.FILMS_URL, json=FILMS)
        m.get('{}/1'.format(ghibli.PEOPLE_URL),
              exc=requests.exceptions.Timeout)
        result = ghibli.fetch_movies_with_people()
        self.assertEqual(result, [])
