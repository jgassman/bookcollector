from django.conf.urls import url

from . import views

app_name = 'moviecollection'
urlpatterns = [
    url(r'^$', views.index, name='view_collection'),
]
