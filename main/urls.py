from django.urls import path
from . import views
from main.views import *

app_name = 'main' 

urlpatterns = [
    path('', GenreList.as_view()),
    path('movies/', MovieList.as_view()),
    path('<str:genre>/', GenreFilmList.as_view()),
    path('<str:genre>/<str:movie>/', MovieReviewList.as_view()),
    
]