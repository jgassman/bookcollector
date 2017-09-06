from django.contrib import admin

from .forms import BookForm
from .models import Author, Book, Series, Genre, Subgenre, Tag


class BookAdmin(admin.ModelAdmin):
    form = BookForm


admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(Series)
admin.site.register(Genre)
admin.site.register(Subgenre)
admin.site.register(Tag)
