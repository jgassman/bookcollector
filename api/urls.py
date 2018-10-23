from django.conf.urls import url

from api import views

app_name = 'api'
urlpatterns = [
    url(r'^authors$', views.AuthorListCreateView.as_view(), name='authors'),
    url(r'^authors/(?P<pk>[0-9]+)$', views.AuthorDetailView.as_view(), name='author_detail'),
]
