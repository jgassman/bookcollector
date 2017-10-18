from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=25)


class Series(models.Model):
    name = models.CharField(max_length=50)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    series = models.ForeignKey(Series)
    series_number = models.IntegerField(null=True, blank=True)
    genre = models.ForeignKey(Genre)

    class Meta:
        unique_together = ('title', 'year',)
        ordering = ['title']
