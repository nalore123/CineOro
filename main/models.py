from django.db import models
from django.utils import timezone
#uvodi se ugradeni user model iz django autentifikacijskog sustava kako 
# bi se recenzije povezale s korisnicima bez kreiranja user modela
from django.contrib.auth.models import User 

class Genre(models.Model):#zanrovi
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Movie(models.Model):#filmovi
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    release_year = models.IntegerField()
    genre = models.ForeignKey(Genre, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Review(models.Model):#model za recenziju
    movie = models.ForeignKey(Movie, default=1, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} --> {self.movie.title}"