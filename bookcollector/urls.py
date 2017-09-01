from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views

urlpatterns = [
    url(r'^bookcollection/', include('bookcollection.urls', namespace='bookcollection')),
    url(r'^gamecollection/', include('gamecollection.urls', namespace='gamecollection')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout', kwargs={'next_page': '/accounts/login'}),
    url(r'^chaining/', include('smart_selects.urls')),
]
