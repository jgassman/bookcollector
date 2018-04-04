from django.contrib import admin

from gamecollection.models import Game, Genre, Franchise, System

admin.site.register(Game)
admin.site.register(Franchise)
admin.site.register(System)
admin.site.register(Genre)
