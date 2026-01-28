import random
from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import *
from main.factory import *

NUM_GENRES = 10
NUM_MOVIES = 20
NUM_USERS = 30
NUM_REVIEWS = 200

class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")#brisu se stari podaci
        models = [Review, Movie, Genre, User]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        for _ in range(NUM_GENRES):
            genre = GenreFactory()

        for _ in range(NUM_MOVIES):
            movie = MovieFactory()

        for _ in range(NUM_USERS):
            user = UserFactory()

        for _ in range(NUM_REVIEWS):
            review = ReviewFactory()
