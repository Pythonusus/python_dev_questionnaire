"""
Project wide fixtures for pytest.
"""

import pytest
from django.contrib.auth import get_user_model

from python_dev_questionnaire.factories import UserFactory

User = get_user_model()


@pytest.fixture
def logged_in_user(client, db):
    """
    Fixture to create a logged in user.
    """
    user = UserFactory()
    client.force_login(user)
    return user
