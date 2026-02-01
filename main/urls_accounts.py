from django.urls import path
from . import views

#poseban url za korisnice racune, registraciju, login, logout
urlpatterns = [
    path('register/', views.register, name='register'),
]
