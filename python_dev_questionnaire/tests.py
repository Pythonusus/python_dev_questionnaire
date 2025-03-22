"""
Tests for the main pages of the website.

Questions index page is tested in questions/tests.py.
Registration page is user related, so it is tested in users/tests.py.
"""

import pytest
from django.urls import path, reverse_lazy

from python_dev_questionnaire.factories import UserFactory


class TestIndexPage:
    def setup_method(self):
        # Common URLs that should be visible to all users
        self.common_urls = [
            'index',
            'questions_index',
            'materials',
            'about',
        ]

    @pytest.mark.django_db
    def test_navbar_with_logged_in_user(self, client, logged_in_user):
        response = client.get(reverse_lazy('index'))
        assert response.status_code == 200
        assert 'index.html' in [t.name for t in response.templates]
        content = response.content.decode()

        # Check common elements
        for url in self.common_urls:
            assert str(reverse_lazy(url)) in content

        # Check logged in specific elements
        assert str(reverse_lazy('logout')) in content
        assert (
            str(reverse_lazy('users_profile', args=[logged_in_user.username]))
            in content
        )

        # Check logged out elements should not be present
        assert str(reverse_lazy('login')) not in content
        assert str(reverse_lazy('users_register')) not in content

    @pytest.mark.django_db
    def test_navbar_with_logged_out_user(self, client, logged_in_user):
        client.logout()
        response = client.get(reverse_lazy('index'))
        assert response.status_code == 200
        assert 'index.html' in [t.name for t in response.templates]
        content = response.content.decode()
        # Check common elements
        for url in self.common_urls:
            assert str(reverse_lazy(url)) in content

        # Check logged out specific elements
        assert str(reverse_lazy('login')) in content
        assert str(reverse_lazy('users_register')) in content

        # Check logged in elements should not be present
        assert str(reverse_lazy('logout')) not in content
        assert (
            str(reverse_lazy('users_profile', args=[logged_in_user.username]))
            not in content
        )


class TestMaterialsPage:
    def test_materials(self, client):
        response = client.get(reverse_lazy('materials'))
        assert response.status_code == 200
        assert 'materials.html' in [t.name for t in response.templates]


class TestAboutPage:
    def test_about(self, client):
        response = client.get(reverse_lazy('about'))
        assert response.status_code == 200
        assert 'about.html' in [t.name for t in response.templates]


class TestThemeSelection:
    def test_theme_selection(self, client):
        # Test setting theme to dark
        response = client.post(reverse_lazy('set_theme', args=['dark']))
        assert response.status_code == 302
        assert 'django_theme' in response.cookies
        assert response.cookies['django_theme'].value == 'dark'

        # Test setting theme to light
        response = client.post(reverse_lazy('set_theme', args=['light']))
        assert response.status_code == 302
        assert 'django_theme' in response.cookies
        assert response.cookies['django_theme'].value == 'light'


class TestLoginPage:
    @pytest.mark.django_db
    def setup_method(self):
        # Create a user with a known raw password
        self.raw_password = 'testpass123'
        self.user = UserFactory.create(username='testuser1')
        # Set the password properly to create the hash
        self.user.set_password(self.raw_password)
        self.user.save()

    @pytest.mark.django_db
    def test_login_get(self, client):
        response = client.get(reverse_lazy('login'))
        assert response.status_code == 200
        assert 'login.html' in [t.name for t in response.templates]

    @pytest.mark.django_db
    def test_login_post_success(self, client):
        response = client.post(
            reverse_lazy('login'),
            data={
                'username': self.user.username,
                # Use the raw password, not the hashed one
                'password': self.raw_password,
            },
        )
        assert response.status_code == 302
        assert response.url == reverse_lazy('index')
        assert self.user.is_authenticated

    @pytest.mark.django_db
    def test_login_post_wrong_password(self, client):
        response = client.post(
            reverse_lazy('login'),
            data={'username': self.user.username, 'password': 'wrongpass'},
        )
        assert response.status_code == 200
        assert 'login.html' in [t.name for t in response.templates]

    @pytest.mark.django_db
    def test_login_post_wrong_username(self, client):
        response = client.post(
            reverse_lazy('login'),
            data={'username': 'wrongusername', 'password': self.raw_password},
        )
        assert response.status_code == 200
        assert 'login.html' in [t.name for t in response.templates]


class TestLogoutPage:
    @pytest.mark.django_db
    def test_logout(self, client, logged_in_user):
        response = client.post(reverse_lazy('logout'))
        assert response.status_code == 302
        assert response.url == reverse_lazy('login')
        next_response = client.get(
            reverse_lazy('users_profile', args=[logged_in_user.username])
        )
        assert next_response.status_code == 302
        assert str(reverse_lazy('login')) in next_response.url


class TestErrorPages:
    def test_404_error(self, client):
        response = client.get('/non-existent-page/', follow=False)
        assert response.status_code == 404
        assert 'errors/404.html' in [t.name for t in response.templates]

    # Settings fixture is used to change django settings for test
    # and revert them after the test.
    def test_500_error(self, client, settings):
        def bad_view(request):
            raise Exception('Test 500 error')

        test_url = [
            path('test-500-error/', bad_view),
        ]

        # Creating a temporary TestUrlconf class, because Django ROOT_URLCONF
        # is expecting a class, or an object, not a list of paths
        class TestUrlconf:
            urlpatterns = test_url

        settings.ROOT_URLCONF = TestUrlconf
        settings.DEBUG = False

        with pytest.raises(Exception):
            response = client.get('/test-500-error/')
            assert response.status_code == 500
            assert 'errors/500.html' in [t.name for t in response.templates]
