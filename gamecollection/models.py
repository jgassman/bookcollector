from django.db import models

AGE_RATING_CHOICES = (
    ('EC', 'Early Childhood'),
    ('K-A', 'Kids to Adults'),
    ('E', 'Everyone'),
    ('E10+', 'Everyone 10+'),
    ('T', 'Teen'),
    ('M', 'Mature'),
    ('GA', 'General Audiences')
)


class Genre(models.Model):
    name = models.CharField(max_length=20)

    @property
    def game_count(self):
        return self.game_set.count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Franchise(models.Model):
    name = models.CharField(max_length=100)

    @property
    def games(self):
        return self.game_set.all()

    @property
    def game_count(self):
        return self.game_set.count()

    @property
    def genre(self):
        try:
            return self.game_set.all()[0].genre
        except:
            return None

    @property
    def systems(self):
        system_set = set()
        for game in self.game_set.all():
            system_set.add(game.system)
        return system_set

    @property
    def genres(self):
        genre_set = set()
        for game in self.game_set.all():
            genre_set.add(game.genre)
        return genre_set

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class System(models.Model):
    name = models.CharField(max_length=100)

    @property
    def games(self):
        return self.game_set.all()

    @property
    def game_count(self):
        return self.game_set.count()

    @property
    def franchises(self):
        franchise_set = set()
        for game in self.games:
            for franchise in game.franchises.all():
                franchise_set.add(franchise)
        return franchise_set

    @property
    def franchise_count(self):
        return len(self.franchises)

    @property
    def genres(self):
        genre_set = set()
        for game in self.game_set.all():
            genre_set.add(game.genre)
        return genre_set

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Game(models.Model):
    title = models.CharField(max_length=100)
    year_released = models.IntegerField()
    age_rating = models.IntegerField()
    age_rating = models.CharField(max_length=15, choices=AGE_RATING_CHOICES, default='E')
    franchises = models.ManyToManyField(Franchise, blank=True)
    system = models.ForeignKey(System)
    genre = models.ForeignKey(Genre)
    copies = models.IntegerField(default=1)
    digital = models.BooleanField(default=False)
    needs_case = models.BooleanField(default=False)
    needs_booklet = models.BooleanField(default=False)
    img_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
