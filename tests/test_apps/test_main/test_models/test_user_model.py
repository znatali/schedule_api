
from hypothesis import given
from hypothesis.extra import django

from server.apps.main.models.user import User


class TestUser(django.TestCase):
    """This is a property-based test that ensures model correctness."""

    @given(django.from_model(User))
    def test_model_properties(self, instance):
        """Tests that instance can be saved and has correct representation."""
        instance.username = 'test-user'
        instance.password = '8pXS#sfCpWX8CB29LsqwmhNWeN'
        instance.save()

        assert instance.id > 0
        assert len(str(instance)) <= 20
