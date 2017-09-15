from .models import AGE_GROUP_CHOICES, Book, Genre


def get_age_group(age_code):
    return [a for a in AGE_GROUP_CHOICES if a[0] == age_code][0]


def get_age_group_books(age):
    return sorted(Book.objects.filter(age_group=age[0]), key=lambda b: b.alphabetical_title)


def get_age_group_authors(age):
    authors = set()
    for b in get_age_group_books(age):
        for a in b.authors.all():
            authors.add(a)
    return sorted(list(authors), key=lambda a: a.last_name)


def get_age_group_books_by_genre(age):
    return {g.name: Book.objects.filter(genre=g, age_group=age[0]) for g in Genre.objects.all()
            if Book.objects.filter(genre=g, age_group=age[0])}
