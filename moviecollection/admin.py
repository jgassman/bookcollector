from django.contrib import admin

from .models import Genre, Series, Movie


admin.site.register(Genre)
admin.site.register(Series)
admin.site.register(Movie)
