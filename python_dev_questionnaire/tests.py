import pytest
from django.urls import reverse_lazy


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
            str(reverse_lazy('profile', args=[logged_in_user.pk])) in content
        )

        # Check logged out elements should not be present
        assert str(reverse_lazy('login')) not in content
        assert str(reverse_lazy('register')) not in content

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
        assert str(reverse_lazy('register')) in content

        # Check logged in elements should not be present
        assert str(reverse_lazy('logout')) not in content
        assert (
            str(reverse_lazy('profile', args=[logged_in_user.pk]))
            not in content
        )


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


class TestRegisterPage:
    def test_register(self, client):
        response = client.get(reverse_lazy('register'))
        assert response.status_code == 200
        assert 'register.html' in [t.name for t in response.templates]


class TestLoginPage:
    def test_login(self, client):
        response = client.get(reverse_lazy('login'))
        assert response.status_code == 200
        assert 'login.html' in [t.name for t in response.templates]


class TestProfilePage:
    @pytest.mark.django_db
    def test_profile(self, client, logged_in_user):
        response = client.get(
            reverse_lazy('profile', args=[logged_in_user.pk])
        )
        assert response.status_code == 200
        assert 'profile.html' in [t.name for t in response.templates]


class TestAboutPage:
    def test_about(self, client):
        response = client.get(reverse_lazy('about'))
        assert response.status_code == 200
        assert 'about.html' in [t.name for t in response.templates]


class TestMaterialsPage:
    def test_materials(self, client):
        response = client.get(reverse_lazy('materials'))
        assert response.status_code == 200
        assert 'materials.html' in [t.name for t in response.templates]
