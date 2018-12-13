from django.contrib import admin

from .forms import BookForm
from .models import Author, Book, Series, Genre, Subgenre, Tag


def store_all(queryset):
    for obj in queryset:
        obj.storage = True
        obj.save()


def store_books(BookAdmin, request, queryset):
    store_all(queryset)
store_books.short_description = 'Move to Storage'


def store_series(SeriesAdmin, request, queryset):
    store_all(queryset)
store_series.short_description = 'Move to Storage'


class BookAdmin(admin.ModelAdmin):
    form = BookForm

    list_filter = ('series',)
    search_fields = ('title',)
    actions = [store_books, ]

class SeriesAdmin(admin.ModelAdmin):

    search_fields = ('name',)
    actions = [store_series, ]


admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Genre)
admin.site.register(Subgenre)
admin.site.register(Tag)
