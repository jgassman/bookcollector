from django.db import models

from smart_selects.db_fields import ChainedForeignKey

FORMAT_CHOICES = (
    ('blu_ray', 'Blu-Ray'),
    ('dvd', 'DVD'),
    ('mixed', 'Blu-Ray/DVD'),
)


class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @property
    def movie_count(self):
        return len(self.movie_set.all())

    class Meta:
        ordering = ['name']


class Genre(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    @property
    def movie_count(self):
        return len(self.movie_set.all())

    class Meta:
        ordering = ['name']


class Subgenre(models.Model):
    name = models.CharField(max_length=25)
    genre = models.ForeignKey(Genre)

    def __str__(self):
        return self.name

    @property
    def movie_count(self):
        return len(self.movie_set.all())

    class Meta:
        ordering = ['name']


class Series(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @property
    def genre(self):
        return self.movie_set.all()[0].genre

    @property
    def movie_count(self):
        return len(self.movie_set.all())

    class Meta:
        verbose_name_plural = 'series'
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    company = models.ForeignKey(Company)
    series = models.ForeignKey(Series, null=True, blank=True)
    series_number = models.IntegerField(null=True, blank=True)
    genre = models.ForeignKey(Genre)
    subgenre = ChainedForeignKey(
        Subgenre,
        chained_field="genre",
        chained_model_field="genre",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True, blank=True)
    disc_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='dvd')
    tv_series = models.BooleanField()
    img_url = models.URLField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    @property
    def alphabetical_title(self):
        title = self.title

        starts_with_flags = ['the ', 'an ', 'a ']

        for flag in starts_with_flags:
            if title.lower().startswith(flag):
                return ("%s, %s" % (title[len(flag):], title[:len(flag)-1])).lower()
        return self.title.lower()

    @property
    def format_str(self):
        return [f[1] for f in FORMAT_CHOICES if f[0] == self.disc_format][0]

    class Meta:
        unique_together = ('title', 'year',)
        ordering = ['title']
