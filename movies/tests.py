from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from movies.models import Movie


class MovieTests(TestCase):
    """
    Automated tests for the Movies app.
    These tests check core functionality:
    - Home page loads correctly
    - Access control on the shelf page
    - Adding movies works
    - Movie status changes work
    """

    def setUp(self):
        """
        This method runs before *every* test.
        We create a test user and a test client.
        """
        self.user = User.objects.create_user(
            username="tester",
            password="password123"
        )
        self.client = Client()

    def test_home_page_loads(self):
        """
        Ensure the home page (movie search page) loads successfully.
        This is a basic health check to confirm the view returns HTTP 200.
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "movies/home.html")

    def test_shelf_redirects_when_not_logged_in(self):
        """
        The shelf page should NOT be accessible to logged-out users.
        This test ensures the view correctly redirects to the login page.
        """
        response = self.client.get(reverse("my_shelf"))
        self.assertEqual(response.status_code, 302)  # Redirect expected

    def test_my_shelf_loads_when_logged_in(self):
        """
        Once the user is logged in, the shelf page should load normally.
        """
        self.client.login(username="tester", password="password123")
        response = self.client.get(reverse("my_shelf"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "movies/shelf.html")

    def test_add_movie_creates_object(self):
        """
        Test the add_to_shelf view.
        When a POST is sent with movie details, a Movie object
        should be created and linked to the logged-in user.
        """
        self.client.login(username="tester", password="password123")

        response = self.client.post(reverse("add_to_shelf"), {
            "tmdb_id": "12345",
            "title": "Test Movie",
            "poster_path": "/abc.jpg",
        })

        # Check movie was created
        self.assertEqual(Movie.objects.count(), 1)

        movie = Movie.objects.first()
        self.assertEqual(movie.title, "Test Movie")
        self.assertEqual(movie.user, self.user)

    def test_change_status(self):
        """
        Test the change_status view.
        Ensures that a movie's status updates correctly via POST.
        """
        self.client.login(username="tester", password="password123")

        movie = Movie.objects.create(
            user=self.user,
            tmdb_id="1",
            title="Test Film",
            status="to_watch",
        )

        # Change status to "watched"
        response = self.client.post(
            reverse("change_status", args=[movie.id, "watched"])
        )

        movie.refresh_from_db()
        self.assertEqual(movie.status, "watched")
