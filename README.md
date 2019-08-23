## Development and testing environments

  - Ubuntu 17.04
  - Docker Compose (1.24.1, build 4667896b)
  - Docker  (1.13.1, build 092cba3)
  - Python docker image (python:3.7-alpine)
  - Redis docker image (redis:alpine)
  - Django (2.2.4)
  - Celery (4.3.0)


## How to start

Make sure that docker-compose and docker are installed on your system. Clone the repository and then change directory to the cloned repository.

Prepare the DB and run the DB migrations:

```sh
docker-compose up init
```

Run the tests (All the tests are located in `ghibli/tests/`):

```sh
docker-compose up test
```

Run the web application, celery worker and celery beat:

```sh
docker-compose up web celery-worker celery-beat
```

You can access the web application from your browser by this URL `http://localhost:8000/movies/`.

**You should see the list of all movies with people. If the list is empty then try to wait for few seconds because fetching data from Ghibli API can take few seconds and then relaod the page again. Or you can read the section "How to read the log" below to know when to reload the page.**

## How it works

There is a task called `ghibli_fetch_movies` in `ghibli/tasks.py` run every 1 minute using Celery. This task fetches the movies from Ghibli API and adds people to their movies and saves the data into Redis.

#### How to read the log
You can follow the log of this command `docker-compose up web celery-worker celery-beat`


  - When the task starts reading the list of movies and their people from the API then you will see this:
```sh
Starting fetching data from API
```
  - When the task completes reading the data from the API and it starts saving the list of movies with people then you will see this:
```sh
Saving data from API
```
  - When the task is completed successfully then you will see this:
```sh
Fetching data succeeded
```

## TODO
  - Add docker production environment.
