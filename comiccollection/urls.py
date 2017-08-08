from django.conf.urls import url

from . import views

app_name = 'comiccollection'
urlpatterns = [
    url(r'^$', views.index, name='view_collection'),
    url(r'^comics/$', views.comics, name='comics'),
    url(r'^illustrators/$', views.illustrators, name='illustrators'),
    url(r'^publishers/$', views.publishers, name='publishers'),
    url(r'^series/$', views.series, name='series'),
    url(r'^writers/$', views.writers, name='writers'),
    url(r'^comics/(?P<comic_id>[0-9]+)/$', views.comic_detail, name='comic_detail'),
    url(r'^illustrators/(?P<illustrator_id>[0-9]+)/$', views.illustrator_detail, name='illustrator_detail'),
    url(r'^publishers/(?P<publisher_id>[0-9]+)/$', views.publisher_detail, name='publisher_detail'),
    url(r'^series/(?P<series_id>[0-9]+)/$', views.series_detail, name='series_detail'),
    url(r'^writers/(?P<writer_id>[0-9]+)/$', views.writer_detail, name='writer_detail'),
    url(r'^comics/new_comic/$', views.comic_create, name='new_comicbook'),
    url(r'^illustrators/new_illustrator/$', views.illustrator_create, name='new_illustrator'),
    url(r'^publishers/new_publisher/$', views.publisher_create, name='new_publisher'),
    url(r'^series/new_series/$', views.series_create, name='new_series'),
    url(r'^writers/new_writer/$', views.writer_create, name='new_writer'),
]
