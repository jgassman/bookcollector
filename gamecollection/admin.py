from django.contrib import admin

from gamecollection.models import Game, Genre, Series, Developer, System

admin.site.register(Game)
admin.site.register(Series)
admin.site.register(Developer)
admin.site.register(System)
admin.site.register(Genre)
