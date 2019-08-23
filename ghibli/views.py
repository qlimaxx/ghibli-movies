from django.conf import settings
from django.shortcuts import render
from django.core.cache import cache


def movies(request):
    movies = cache.get(settings.GHIBLI_CACHE_KEY, [])
    return render(request, 'ghibli/movies.html', {'movies': movies})
