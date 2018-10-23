from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^bookcollection/', include('bookcollection.urls', namespace='bookcollection')),
    url(r'^gamecollection/', include('gamecollection.urls', namespace='gamecollection')),
    url(r'^moviecollection/', include('moviecollection.urls', namespace='moviecollection')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout', kwargs={'next_page': '/accounts/login'}),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'', include('landingpage.urls', namespace='landingpage')),
]
