from django.contrib import admin

from .models import Genre, Series, Movie, Subgenre, Tag


admin.site.register(Genre)
admin.site.register(Subgenre)
admin.site.register(Series)
admin.site.register(Movie)
admin.site.register(Tag)
