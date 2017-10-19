from django.conf.urls import url

from . import views

app_name = 'moviecollection'
urlpatterns = [
    url(r'^$', views.index, name='view_collection'),
    url(r'^movies/$', views.movies, name='movies'),
    url(r'^movies/(?P<movie_id>[0-9]+)/$', views.movie_detail, name='movie_detail'),
    url(r'^movies/genre/(?P<genre_id>[0-9]+)/$', views.genre_movies, name='genre_movies'),
    url(r'^genres/$', views.genres, name='genres'),
    url(r'^genres/(?P<genre_id>[0-9]+)/$', views.genre_detail, name='genre_detail'),
    url(r'^series/$', views.series, name='series'),
    url(r'^series/(?P<series_id>[0-9]+)/$', views.series_detail, name='series_detail'),
    url(r'^series/genre/(?P<genre_id>[0-9]+)/$', views.genre_series, name='genre_series'),
]
