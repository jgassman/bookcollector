from django.db import models

from smart_selects.db_fields import ChainedForeignKey


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


class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    series = models.ForeignKey(Series, null=True, blank=True)
    series_number = models.IntegerField(null=True, blank=True)
    genre = models.ForeignKey(Genre)
    subgenre = ChainedForeignKey(
        Subgenre,
        chained_field="genre",
        chained_model_field="genre",
        show_all=False,
        auto_choose=True,
        sort=True)
    img_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def alphabetical_title(self):
        title = self.title

        starts_with_flags = ['the ', 'an ', 'a ']

        for flag in starts_with_flags:
            if title.lower().startswith(flag):
                return ("%s, %s" % (title[len(flag):], title[:len(flag)-1])).lower()
            else:
                pass
        return self.title.lower()

    class Meta:
        unique_together = ('title', 'year',)
        ordering = ['title']
