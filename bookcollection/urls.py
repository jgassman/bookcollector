from django.conf.urls import url

from . import views

app_name = 'bookcollection'
urlpatterns = [
    url(r'^$', views.index, name='view_collection'),
    url(r'^authors/$', views.authors, name='authors'),
    url(r'^authors/(?P<author_id>[0-9]+)/$', views.author_detail, name='author_detail'),
    url(r'^authors/genre/(?P<genre_id>[0-9]+)/$', views.genre_authors, name='genre_authors'),
    url(r'^authors/by_age/(?P<age_code>\w+)/$', views.age_authors, name='age_authors'),
    url(r'^books/$', views.books, name='books'),
    url(r'^books/(?P<book_id>[0-9]+)/$', views.book_detail, name='book_detail'),
    url(r'^books/author/(?P<author_id>[0-9]+)/$', views.author_books, name='author_books'),
    url(r'^books/genre/(?P<genre_id>[0-9]+)/$', views.genre_books, name='genre_books'),
    url(r'^books/by_age/(?P<age_code>\w+)/$', views.age_books, name='age_books'),
    url(r'^books/unread$', views.unread, name='unread'),
    url(r'^genres/$', views.genres, name='genres'),
    url(r'^genres/(?P<genre_id>[0-9]+)/$', views.genre_detail, name='genre_detail'),
    url(r'^genres/author/(?P<author_id>[0-9]+)/$', views.author_genres, name='author_genres'),
    url(r'^series/$', views.series, name='series'),
    url(r'^series/(?P<series_id>[0-9]+)/$', views.series_detail, name='series_detail'),
    url(r'^series/author/(?P<author_id>[0-9]+)/$', views.author_series, name='author_series'),
    url(r'^series/genre/(?P<genre_id>[0-9]+)/$', views.genre_series, name='genre_series'),
    url(r'^series/by_age/(?P<age_code>\w+)/$', views.age_series, name='age_series'),
    url(r'^tags/$', views.tags, name='tags'),
    url(r'^tags/(?P<tag_id>[0-9]+)/$', views.tag_detail, name='tag_detail'),
    url(r'^by_age/$', views.ages, name='ages'),
    url(r'^by_age/(?P<age_code>\w+)/$', views.age_detail, name='age_detail'),
]
