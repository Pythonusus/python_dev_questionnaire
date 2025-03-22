import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

# from python_dev_questionnaire.factories import UserFactory

User = get_user_model()


class TestRegisterPage:
    def test_register_get(self, client):
        response = client.get(reverse_lazy('users_register'))
        assert response.status_code == 200
        assert 'users/register.html' in [t.name for t in response.templates]

    @pytest.mark.django_db
    def test_register_post_success(self, client):
        response = client.post(
            reverse_lazy('users_register'),
            data={
                'username': 'testuser1',
                'email': 'testuser1@example.com',
                'password1': 'testpass!123',
                'password2': 'testpass!123',
            },
        )
        assert response.status_code == 302
        assert response.url == reverse_lazy('login')
        created_user = User.objects.get(username='testuser1')
        assert created_user.email == 'testuser1@example.com'


class TestProfilePage:
    @pytest.mark.django_db
    def test_profile(self, client, logged_in_user):
        response = client.get(
            reverse_lazy('users_profile', args=[logged_in_user.username])
        )
        assert response.status_code == 200
        assert 'users/profile.html' in [t.name for t in response.templates]
