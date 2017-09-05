from django.conf.urls import url

from . import views

app_name = 'bookcollection'
urlpatterns = [
    url(r'^$', views.index, name='view_collection'),
    url(r'^authors/$', views.authors, name='authors'),
    url(r'^authors/(?P<author_id>[0-9]+)/$', views.author_detail, name='author_detail'),
    url(r'^authors/genre/(?P<genre_id>[0-9]+)/$', views.genre_authors, name='genre_authors'),
    url(r'^books/$', views.books, name='books'),
    url(r'^books/(?P<book_id>[0-9]+)/$', views.book_detail, name='book_detail'),
    url(r'^books/genre/(?P<genre_id>[0-9]+)/$', views.genre_books, name='genre_books'),
    url(r'^genres/$', views.genres, name='genres'),
    url(r'^genres/(?P<genre_id>[0-9]+)/$', views.genre_detail, name='genre_detail'),
    url(r'^series/$', views.series, name='series'),
    url(r'^series/(?P<series_id>[0-9]+)/$', views.series_detail, name='series_detail'),
    url(r'^series/genre/(?P<genre_id>[0-9]+)/$', views.genre_series, name='genre_series'),
]
