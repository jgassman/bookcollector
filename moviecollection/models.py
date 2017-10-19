from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=25)

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
    series = models.ForeignKey(Series)
    series_number = models.IntegerField(null=True, blank=True)
    genre = models.ForeignKey(Genre)
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
