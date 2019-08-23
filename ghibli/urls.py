from django.urls import path

from . import views


app_name = 'ghibli'

urlpatterns = [
    path('movies/', views.movies, name='movies'),
]
