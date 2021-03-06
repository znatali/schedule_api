# -*- coding: utf-8 -*-

import secrets

from hypothesis import given
from hypothesis.extra import django

from server.apps.main.models.user import User

TEST_USERNAME = 'tester'
TEST_USER_EMAIL = 'tester@example.com'
TEST_FIRST_NAME = 'John'
TEST_LAST_NAME = 'Smith'
TEST_USER_PASSWORD = f'{secrets.token_hex(25)}#Ak'


class TestUser(django.TestCase):
    """This is a property-based test that ensures model correctness."""

    @given(django.from_model(User))
    def test_model_properties(self, instance):
        """Tests that instance can be saved and has correct representation."""
        instance.username = TEST_USERNAME
        instance.password = TEST_USER_PASSWORD
        instance.save()

        assert instance.id > 0
        assert len(str(instance)) <= 20
