from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=15)

    @property
    def comic_count(self):
        return ComicBook.objects.filter(genre=self).count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Writer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    @property
    def comic_count(self):
        return ComicBook.objects.filter(writers=self).count()

    @property
    def publishers(self):
        publisher_set = set()
        for book in self.comicbook_set.all():
            publisher_set.add(book.genre)
        return publisher_set

    @property
    def series(self):
        series_set = set()
        for book in self.comicbook_set.all():
            if book.series:
                series_set.add(book.series)
        return series_set

    @property
    def publisher_count(self):
        return len(self.publishers)

    @property
    def series_count(self):
        return len(self.series)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        ordering = ['last_name', 'first_name']


class Illustrator(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    @property
    def comic_count(self):
        return ComicBook.objects.filter(illustrators=self).count()

    @property
    def publishers(self):
        publisher_set = set()
        for book in self.comicbook_set.all():
            publisher_set.add(book.genre)
        return publisher_set

    @property
    def series(self):
        series_set = set()
        for book in self.comicbook_set.all():
            if book.series:
                series_set.add(book.series)
        return series_set

    @property
    def publisher_count(self):
        return len(self.publishers)

    @property
    def series_count(self):
        return len(self.series)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        ordering = ['last_name', 'first_name']


class Publisher(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @property
    def series(self):
        series_set = set()
        for book in self.comicbook_set.all():
            if book.series:
                series_set.add(book.series)
        return series_set

    @property
    def series_count(self):
        return len(self.series)

    @property
    def comic_count(self):
        return ComicBook.objects.filter(publisher=self).count()


class Series(models.Model):
    name = models.CharField(max_length=50)

    @property
    def comic_count(self):
        return ComicBook.objects.filter(series=self).count()

    @property
    def writers(self):
        writers = set()
        for book in ComicBook.objects.filter(series=self):
            [writers.add(a) for a in book.writers.all()]
        return writers

    @property
    def illustrators(self):
        illustrators = set()
        for book in ComicBook.objects.filter(series=self):
            [illustrators.add(a) for a in book.illustrators.all()]
        return illustrators

    def __str__(self):
        return self.name

    @property
    def genre(self):
        try:
            return ComicBook.objects.filter(series=self)[0].genre
        except:
            return None

    class Meta:
        verbose_name_plural = "Series"
        ordering = ['name']


class ComicBook(models.Model):
    title = models.CharField(max_length=100)
    year_published = models.IntegerField()
    writers = models.ManyToManyField(Writer)
    illustrators = models.ManyToManyField(Illustrator)
    publisher = models.ForeignKey(Publisher)
    series = models.ForeignKey(Series, models.SET_NULL, blank=True, null=True)
    series_number = models.CharField(max_length=10, blank=True, null=True)
    genre = models.ForeignKey(Genre)
    collection = models.BooleanField()
    img_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
