import requests


BASE_URL = 'https://ghibliapi.herokuapp.com'
FILMS_URL = '{}/films'.format(BASE_URL)
PEOPLE_URL = '{}/people'.format(BASE_URL)
TIMEOUT = 15


def fetch_movies_with_people():
    films = []
    try:
        response_films = requests.get(
            FILMS_URL, params={
                'limit': 250}, timeout=TIMEOUT)
    except requests.exceptions.RequestException:
        return []
    if response_films.ok:
        for film in response_films.json():
            people = []
            if film['people'] == ['{}/'.format(PEOPLE_URL)]:
                try:
                    response = requests.get(
                        PEOPLE_URL, params={
                            'limit': 250}, timeout=TIMEOUT)
                except requests.exceptions.RequestException:
                    return []
                if response.ok:
                    for elem in response.json():
                        # Check if film exists in person films
                        if '{0}/{1}'.format(FILMS_URL,
                                            film['id']) in elem['films']:
                            people.append(elem)
                else:
                    return []
            else:
                for url in film['people']:
                    try:
                        response = requests.get(url, timeout=TIMEOUT)
                    except requests.exceptions.RequestException:
                        return []
                    if response.ok:
                        people.append(response.json())
                    else:
                        return []
            film['people'] = people
            films.append(film)
    else:
        return []
    return films
