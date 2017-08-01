from django.db import models

AGE_GROUP_CHOICES = (
    ('Children', 'Children'),
    ('Middle Grade', 'Middle Grade'),
    ('Young Adult', 'Young Adult'),
    ('Adult', 'Adult')
)


class Genre(models.Model):
    name = models.CharField(max_length=15)

    @property
    def book_count(self):
        return Book.objects.filter(genre=self).count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Subgenre(models.Model):
    name = models.CharField(max_length=15)
    genre = models.ForeignKey(Genre)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'genre']


class Author(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)

    @property
    def book_count(self):
        return Book.objects.filter(authors=self).count()

    @property
    def genres(self):
        genre_set = set()
        for book in self.book_set.all():
            genre_set.add(book.genre)
        return genre_set

    @property
    def series(self):
        series_set = set()
        for book in self.book_set.all():
            if book.series:
                series_set.add(book.series)
        return series_set

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
        ordering = ['last_name', 'first_name']


class Series(models.Model):
    name = models.CharField(max_length=50)

    @property
    def book_count(self):
        return Book.objects.filter(series=self).count()

    @property
    def genre(self):
        try:
            return Book.objects.filter(series=self, series_number=1)[0].genre
        except:
            return None

    @property
    def subgenre(self):
        try:
            return Book.objects.filter(series=self, series_number=1)[0].subgenre
        except:
            return None

    @property
    def authors(self):
        authors = set()
        for book in Book.objects.filter(series=self):
            [authors.add(a) for a in book.authors.all()]
        return authors

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
    subgenre = models.ForeignKey(Subgenre, null=True, blank=True)
    age_group = models.CharField(max_length=15, choices=AGE_GROUP_CHOICES, default='Children')
    audiobook = models.BooleanField()
    img_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
