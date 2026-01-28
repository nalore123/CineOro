import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from django.utils import timezone
from .models import *
#za name sam prije stavila word, ali kada bih stavila word dobila 
# bih neke random rijeci koje uopce ne predstavljaju zanrove
#zbog toga sam napravila listu sa mogucim zanrovima koji se koriste 
# za ime i radi se globalno
GENRES = [
    "Action","Adventure", "Animation", "Biography", "Comedy", "Crime",
    "Documentary", "Drama", "Family", "Fantasy", "History", "Horror",
    "Music", "Musical", "Mystery", "Romance", "Sci-Fi",
    "Sport", "Thriller", "War", "Western"
    ]
class GenreFactory(DjangoModelFactory):
    class Meta:
        model = Genre
    name = factory.Iterator(GENRES)
    description = factory.Faker("sentence", nb_words=10)

class MovieFactory(DjangoModelFactory):
    class Meta:
        model = Movie
    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=3)
    release_year = factory.Faker("year")
    genre = factory.Iterator(Genre.objects.all())#stvaranje veze sa žanrom za kreiranje radnom genre

#kreiranje objekata iz django ugradenog user modela
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    #PostGenerationMethodCall poziva metodu set password nakon kreiranja objekta
    #lozinka pravilno hashirana, svi tesni korisnici imaju istu lozinku, a username i email su nasumicni
    password = factory.PostGenerationMethodCall('set_password', 'lozinka123')  # svi testni useri imaju istu lozinku

class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review
    movie = factory.Iterator(Movie.objects.all())# stvaranje veze s filmom
    user = factory.Iterator(User.objects.all())#stvaranje veze sa korisnikom
    rating = factory.Faker("random_int", min=1, max=5)
    comment = factory.Faker("paragraph", nb_sentences=2)
    #tzinfo odreduje vremensku zonu
    created_at = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())