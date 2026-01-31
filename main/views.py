from django.shortcuts import render, redirect
from django.views.generic import ListView
from main.models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

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
        self.movie_obj = get_object_or_404(Movie, title=self.kwargs['movie'])
        return Review.objects.filter(movie=self.movie_obj)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = self.movie_obj 
        return context
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

# dodavanje recenzija preko my reviews
@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'main/my_reviews.html', {'reviews': reviews})

@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('main:my_reviews')
    else:
        form = ReviewForm()

    return render(request, 'main/review_form.html', {'form': form})

@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('main:my_reviews')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'main/review_form.html', {'form': form})

@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)

    if request.method == 'POST':
        review.delete()
        return redirect('main:my_reviews')

    return render(request, 'main/review_confirm_delete.html', {'review': review})

# dodavanje recenzija preko prikaza ostalih recenzija
@login_required
def add_review_for_movie(request, movie):
    movie_obj = get_object_or_404(Movie, title=movie)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie_obj
            review.save()
            return redirect('main:my_reviews')  
    else:
        form = ReviewForm()

    return render(request, 'main/review_form.html', {'form': form, 'movie': movie_obj})
