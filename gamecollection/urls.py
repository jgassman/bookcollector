from django.conf.urls import url

from . import views

app_name = 'gameccollection'
urlpatterns = [
    url(r'^$', views.index, name='view_collection'),
    url(r'^games/$', views.games, name='games'),
    url(r'^genres/$', views.genres, name='genres'),
    url(r'^games/new_game/$', views.new_game, name='new_game'),
    url(r'^games/(?P<game_id>[0-9]+)/$', views.game_detail, name='game_detail'),
    url(r'^genres/(?P<genre_id>[0-9]+)/$', views.genre_detail, name='genre_detail'),
    url(r'^series/$', views.series, name='series'),
    url(r'^series/new_series/$', views.new_series, name='new_series'),
    url(r'^series/(?P<series_id>[0-9]+)/$', views.series_detail, name='series_detail'),
    url(r'^developers/$', views.developers, name='developers'),
    url(r'^developers/new_developer/$', views.new_developer, name='new_developer'),
    url(r'^developers/(?P<developer_id>[0-9]+)/$', views.developer_detail, name='developer_detail'),
    url(r'^systems/$', views.systems, name='systems'),
    url(r'^systems/new_system/$', views.new_system, name='new_system'),
    url(r'^systems/(?P<system_id>[0-9]+)/$', views.system_detail, name='system_detail'),
]
