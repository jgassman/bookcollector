from django.contrib import admin

from gamecollection.models import Game, Genre, Series, Studio, System

admin.site.register(Game)
admin.site.register(Series)
admin.site.register(Studio)
admin.site.register(System)
admin.site.register(Genre)
