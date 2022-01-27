import json

from bookcollection import models

book_list = []
for book in models.Book.objects.all():
    book_obj = {
        'title': book.title,
        'year': book.year_published,
        'authors': [
            {
                'first_name': author.first_name,
                'last_name': author.last_name,
            }
            for author in book.authors.all()
        ],
        'series': {'name': book.series.name} if book.series else None,
        'series_number': book.series_number,
        'genre': {'name': book.genre.name},
        'subgenre': {'name': book.subgenre.name, 'genre': {'name': book.subgenre.genre.name}},
        'age_group': book.age_group,
        'audiobook': book.audiobook,
        'read': book.read,
        'storage': book.storage,
        'cover_url': book.img_url,
        'tags': [{'name': tag.name} for tag in book.tags.all()],
    }
    book_list.append(book_obj)

print(json.dumps(book_list))
