# -*- coding: utf-8 -*-

from hypothesis import given
from hypothesis.extra import django

from server.apps.main.models.teacher import Teacher

TEST_TITLE = 'Test'


class TestTeacher(django.TestCase):
    """This is a property-based test that ensures model correctness."""

    @given(django.from_model(Teacher))
    def test_model_properties(self, instance):
        """Tests that instance can be saved and has correct representation."""
        instance.first_name = TEST_TITLE
        instance.last_name = TEST_TITLE
        instance.middle_name = TEST_TITLE
        instance.save()

        assert instance.id > 0
        assert len(str(instance)) <= 20
