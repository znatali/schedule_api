# -*- coding: utf-8 -*-

import json
import secrets

from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from server.apps.main.models.user import User

TEST_USERNAME = 'tester'
TEST_USER_EMAIL = 'tester@example.com'
TEST_FIRST_NAME = 'John'
TEST_LAST_NAME = 'Smith'
TEST_USER_PASSWORD = f'{secrets.token_hex(25)}#Ak'


def test_user(admin_client, admin_user):
    """Create User."""
    # Create without password should fail.
    response = admin_client.post(
        '/user/',
        {
            'email': TEST_USER_EMAIL,
            'first_name': TEST_FIRST_NAME,
            'last_name': TEST_LAST_NAME,
            'username': TEST_USERNAME,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {'password': [ErrorDetail(string='This field is required.', code='required')]}

    # Create should be successful.
    response = admin_client.post(
        '/user/',
        {
            'email': TEST_USER_EMAIL,
            'first_name': TEST_FIRST_NAME,
            'last_name': TEST_LAST_NAME,
            'username': TEST_USERNAME,
            'password': TEST_USER_PASSWORD,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Update should be successful.
    tester = User.objects.get(id=response.data['id'])
    response = admin_client.patch(
        f'/user/{tester.pk}/',
        json.dumps({
            'first_name': f'{TEST_FIRST_NAME}22',
        }),
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == f'{TEST_FIRST_NAME}22'
