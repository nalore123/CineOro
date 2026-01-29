from django.shortcuts import render
from django.views.generic import ListView
from main.models import *
from django.shortcuts import get_object_or_404

# Create your views here.

class MovieList(ListView):
    model = Movie
    template_name='main/movies_by_genre.html'

class GenreList(ListView):
    model = Genre

class GenreFilmList(ListView):
    template_name = 'main/movies_by_genre.html'

    def get_queryset(self):
        self.genre = get_object_or_404(Genre, name=self.kwargs['genre'])
        return Movie.objects.filter(genre=self.genre)
    
class MovieReviewList(ListView):
    template_name = 'main/reviews_by_movie.html'

    def get_queryset(self):
        self.movie = get_object_or_404(Movie, title=self.kwargs['movie'])
        return Review.objects.filter(movie=self.movie)
