from django.contrib import admin
from .models import *

# Register your models here.

model_list = [Genre, Movie, Review]
admin.site.register(model_list)