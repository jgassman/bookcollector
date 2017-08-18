from django.conf.urls import url

from . import views

app_name = 'gameccollection'
urlpatterns = [
    url(r'^$', views.index, name='view_collection'),
    url(r'^games/$', views.games, name='games'),
    url(r'^genres/$', views.genres, name='genres'),
    url(r'^games/(?P<game_id>[0-9]+)/$', views.game_detail, name='game_detail'),
    url(r'^genres/(?P<genre_id>[0-9]+)/$', views.genre_detail, name='genre_detail'),
    url(r'^franchises/$', views.franchises, name='franchises'),
    url(r'^franchises/(?P<franchise_id>[0-9]+)/$', views.franchise_detail, name='franchise_detail'),
    url(r'^developers/$', views.developers, name='developers'),
    url(r'^developers/(?P<developer_id>[0-9]+)/$', views.developer_detail, name='developer_detail'),
    url(r'^systems/$', views.systems, name='systems'),
    url(r'^systems/(?P<system_id>[0-9]+)/$', views.system_detail, name='system_detail'),
]
