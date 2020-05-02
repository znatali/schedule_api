
import pytest

from server.apps.main.urls import app_name

TEST_PASSWORD = '8pXS#sfCpWX8CB29LsqwmhNWeN'


def test_initial0001(migrator):
    """Tests the initial migration forward application."""
    old_state = migrator.before((app_name, None))
    with pytest.raises(LookupError):
        # This model does not exist before this migration:
        old_state.apps.get_model(app_name, 'User')

    new_state = migrator.after((app_name, '0001_initial'))
    model = new_state.apps.get_model(app_name, 'User')

    assert model.objects.create(username='user-test', password=TEST_PASSWORD)
