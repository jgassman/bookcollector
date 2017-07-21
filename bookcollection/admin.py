from django.contrib import admin

from .models import Author, Book, Series, Genre, Subgenre

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Series)
admin.site.register(Genre)
admin.site.register(Subgenre)
