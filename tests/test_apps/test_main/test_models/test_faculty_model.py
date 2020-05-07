# -*- coding: utf-8 -*-

from hypothesis import given
from hypothesis.extra import django

from server.apps.main.models.faculty import Faculty

TEST_TITLE = 'Test'


class TestFaculty(django.TestCase):
    """This is a property-based test that ensures model correctness."""

    @given(django.from_model(Faculty))
    def test_model_properties(self, instance):
        """Tests that instance can be saved and has correct representation."""
        instance.title = TEST_TITLE
        instance.save()

        assert instance.id > 0
        assert len(str(instance)) <= 20
