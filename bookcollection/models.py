import re

from django.db import models

from smart_selects.db_fields import ChainedForeignKey

AGE_GROUP_CHOICES = (
    ('children', 'Children'),
    ('middle_grade', 'Middle Grade'),
    ('young_adult', 'Young Adult'),
    ('adult', 'Adult')
)


class Genre(models.Model):
    name = models.CharField(max_length=25)

    @property
    def book_count(self):
        return Book.objects.filter(genre=self).count()

    @property
    def sorted_books(self):
        return list(self.book_set.all().order_by('alphabetical_title'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Subgenre(Genre):
    genre = models.ForeignKey(Genre)

    class Meta:
        ordering = ['name', 'genre']


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Author(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)

    @property
    def book_count(self):
        return Book.objects.filter(authors=self).count()

    @property
    def sorted_books(self):
        return list(self.book_set.all().order_by('alphabetical_title'))

    @property
    def genres(self):
        return set((book.genre for book in self.book_set.all()))

    @property
    def series(self):
        return set((book.series for book in self.book_set.all() if book.series))

    @property
    def genre_count(self):
        return len(self.genres)

    @property
    def series_count(self):
        return len(self.series)

    def __str__(self):
        if self.first_name:
            return self.first_name + ' ' + self.last_name
        return self.last_name

    class Meta:
        unique_together = ('first_name', 'last_name',)
        ordering = ['last_name', 'first_name']


class Series(models.Model):
    name = models.CharField(max_length=50)

    @property
    def book_count(self):
        return Book.objects.filter(series=self).count()

    @property
    def genre(self):
        try:
            return Book.objects.filter(series=self)[0].genre
        except:
            return None

    @property
    def subgenre(self):
        try:
            return Book.objects.filter(series=self)[0].subgenre
        except:
            return None

    @property
    def authors(self):
        return set((a for book in Book.objects.filter(series=self) for a in book.authors.all()))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Series"
        ordering = ['name']


class Book(models.Model):
    title = models.CharField(max_length=100)
    year_published = models.IntegerField()
    authors = models.ManyToManyField(Author)
    series = models.ForeignKey(Series, models.SET_NULL, blank=True, null=True)
    series_number = models.IntegerField(blank=True, null=True)
    genre = models.ForeignKey(Genre, null=True)
    subgenre = ChainedForeignKey(
        Subgenre,
        chained_field="genre",
        chained_model_field="genre",
        show_all=False,
        auto_choose=True,
        sort=True)
    age_group = models.CharField(max_length=15, choices=AGE_GROUP_CHOICES, default='Children')
    audiobook = models.BooleanField()
    read = models.BooleanField()
    img_url = models.URLField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    @property
    def age(self):
        return [a for a in AGE_GROUP_CHOICES if a[0] == self.age_group][0][1]

    @property
    def alphabetical_title(title):
        title = title.lower()
        prefixes = ('the ', 'an ', 'a ')
        matcher = re.compile('|'.join(map(re.escape, prefixes))).match
        prefix = matcher(title)
        if prefix is not None:
            return "{}, {}".format(title[len(prefix.group()):], prefix.group().strip())
        return title

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'year_published',)
        ordering = ['title']
