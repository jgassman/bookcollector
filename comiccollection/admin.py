from django.contrib import admin

from .models import ComicBook, Genre, Illustrator, Publisher, Series, Writer

admin.site.register(ComicBook)
admin.site.register(Genre)
admin.site.register(Illustrator)
admin.site.register(Publisher)
admin.site.register(Series)
admin.site.register(Writer)
