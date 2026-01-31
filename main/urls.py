from django.urls import path
from . import views
from main.views import *

app_name = 'main' 

urlpatterns = [
    path('', GenreList.as_view()),
    path('movies/', MovieList.as_view()),
    
    path('my-reviews/', views.my_reviews, name='my_reviews'),
    path('reviews/add/', views.add_review, name='add_review'),
    path('reviews/<int:pk>/edit/', views.edit_review, name='edit_review'),
    path('reviews/<int:pk>/delete/', views.delete_review, name='delete_review'),
 
    path('movies/<str:movie>/add-review/', views.add_review_for_movie, name='add_review_for_movie'),
    
    path('<str:genre>/', GenreFilmList.as_view()),
    path('<str:genre>/<str:movie>/', MovieReviewList.as_view()),
    
]