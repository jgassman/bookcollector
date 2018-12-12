from django.contrib import admin

from .forms import BookForm
from .models import Author, Book, Series, Genre, Subgenre, Tag


def store_books(BookAdmin, request, queryset):
    for book in queryset:
        book.storage = True
        book.save()
store_books.short_description = 'Move to Storage'


class BookAdmin(admin.ModelAdmin):
    form = BookForm

    list_filter = ('series',)
    search_fields = ('title',)
    actions = [store_books, ]


admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(Series)
admin.site.register(Genre)
admin.site.register(Subgenre)
admin.site.register(Tag)
