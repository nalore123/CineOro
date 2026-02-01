from django.test import TestCase, Client
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import *
from django.contrib.auth.models import User
from main.models import *
# Create your tests here.

#najprije se testiraju urlovi gdje se pregledava ako urlovi vode na točan view
class TestUrls(SimpleTestCase):

    #url homepage, tj /
    def test_homepage_url_is_resolved(self):
        url = '/'
        #resolve vraća view koji se koristi za zadani url
        #assertequal provjerava da li je taj view genrelist
        self.assertEqual(resolve(url).func.view_class, GenreList)
    
    #url za listu filmova
    def test_movies_url_is_resolved(self):
        url = '/movies/'
        self.assertEqual(resolve(url).func.view_class, MovieList)
    
    def test_my_reviews_url_is_resolved(self):
        url = reverse('main:my_reviews')#reverse generira url po imenu
        self.assertEqual(resolve(url).func, my_reviews)
    
    def test_add_review_url_is_resolved(self):
        url = reverse('main:add_review')
        self.assertEqual(resolve(url).func, add_review)

    def test_edit_review_url_is_resolved(self):
        url = reverse('main:edit_review', args=[1])#url s parametrom pk=1, služi za popunjavanje parametara urla
        self.assertEqual(resolve(url).func, edit_review)

    def test_delete_review_url_is_resolved(self):
        url = reverse('main:delete_review', args=[1])
        self.assertEqual(resolve(url).func, delete_review)

    def test_add_review_for_movie_url_is_resolved(self):
        url = reverse('main:add_review_for_movie', args=['inception'])
        self.assertEqual(resolve(url).func, add_review_for_movie)

    def test_genre_films_url_is_resolved(self):
        url = '/action/'#dinamički url
        self.assertEqual(resolve(url).func.view_class, GenreFilmList)

    def test_movie_reviews_url_is_resolved(self):
        url = '/action/inception/'
        self.assertEqual(resolve(url).func.view_class, MovieReviewList)

#testiranje viewa, vraća se status 200, koristi li se ispravan template
#provjerava ako radi login_required
class TestViews(TestCase):
    
    #izvršava se prije svakog testa, služi za pripremu testne baze i klijenta
    def setUp(self):
        #simulirani web preglednik, omogućava da se 
        # u testu naprave http get ili post zahtjevi za viewe
        self.client = Client()

        #kreira se testni žanr
        self.genre = Genre.objects.create(
            name='Action',
            description='Action movies'
        )

        #kreira se tesni film koji se povezuje sa zanrom
        self.movie = Movie.objects.create(
            title='Inception',
            description='Test movie',
            release_year=2010,
            genre=self.genre
        )

        #stvara se testni korisnik za login_required viewove
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        #kreira se tesna recenzija
        self.review = Review.objects.create(
            movie=self.movie,
            user=self.user,
            rating=5,
            comment='Great movie!'
        )
    #testira se homepage, genrelist, provjerava ako stranica radi
    def test_genre_list_view_GET(self):
        response = self.client.get('/')#simulira korisnika koji ide na /, get zahtjev za /
        self.assertEqual(response.status_code, 200)#provjerava se ako je sve dobro

    #lista filmova --> movielist, ako test radi i ako je template točan
    def test_movie_list_view_GET(self):
        response = self.client.get('/movies/')
        self.assertEqual(response.status_code, 200)
        #gleda se ako je template ispravan
        self.assertTemplateUsed(response, 'main/movies_by_genre.html')

    #prikaz filmova po zanru --> genrefilmlist, prikazuju se filmovi za zanr action
    def test_genre_film_list_view(self):
        response = self.client.get('/Action/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/movies_by_genre.html')

    #prikaz recenzija filma --> moviereviewlist, prikaz recezija filma inception
    def test_movie_review_list_view(self):
        response = self.client.get('/Action/Inception/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/reviews_by_movie.html')

    #login required: bez prijave se redirecta na login, ne može vidjeti my_reviews stranicu
    def test_my_reviews_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('main:my_reviews'))
        self.assertEqual(response.status_code, 302)#found / redirected, ide na stranicu login

    #login_required s prijavom --> status i provjera templatea
    #najprije se simulira login testnog korisnika
    #ide se na my_reviews vievw, status je 200 i može ju vidjeti 
    def test_my_reviews_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:my_reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/my_reviews.html')

#testiranje models.py
class TestModels(TestCase):

    def setUp(self):
        #kreiramo testnog korisnika
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        #kreiramo testni žanr
        self.genre = Genre.objects.create(
            name='Action',
            description='Action movies'
        )

        #kreiramo testni film
        self.movie = Movie.objects.create(
            title='Inception',
            description='A test movie',
            release_year=2010,
            genre=self.genre
        )

        #kreiramo testnu recenziju
        self.review = Review.objects.create(
            movie=self.movie,
            user=self.user,
            rating=5,
            comment='Great movie!'
        )

    #testiranje zanrova, provjerava se da su name i description ispravni
    #provjera se ako str vraca naziv zanra
    def test_genre_creation(self):
        self.assertEqual(self.genre.name, 'Action')
        self.assertEqual(self.genre.description, 'Action movies')
        self.assertEqual(str(self.genre), 'Action')

    #testiranje za filmove
    def test_movie_creation(self):
        self.assertEqual(self.movie.title, 'Inception')
        self.assertEqual(self.movie.description, 'A test movie')
        self.assertEqual(self.movie.release_year, 2010)
        self.assertEqual(self.movie.genre, self.genre)
        self.assertEqual(str(self.movie), 'Inception')

    # testiranje recenzije
    def test_review_creation(self):
        self.assertEqual(self.review.movie, self.movie)
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, 'Great movie!')
        self.assertEqual(str(self.review), 'testuser --> Inception') 