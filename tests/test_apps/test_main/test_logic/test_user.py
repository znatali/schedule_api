# -*- coding: utf-8 -*-

import json
import secrets
from unittest import mock

import pytest
from django.contrib import auth
from rest_framework import status
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.permissions import AllowAny

from server.apps.main.logic.user_base_serializer import UserSerializerBase
from server.apps.main.models.user import User
from server.apps.main.views.user import UserViewSet

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
    assert response.data == {
        'password': [ErrorDetail(string='This field is required.', code='required')],
        'status_code': 400,
    }

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

    # List should be successful.
    response = admin_client.get('/user/')
    assert response.status_code == status.HTTP_200_OK


def test_record_modified(admin_client, admin_user):
    """Update user on race condition should fail."""
    response = admin_client.get(f'/user/{admin_user.pk}/')
    assert response.status_code == 200, response.content
    initial_version = json.loads(response.content)['version']

    response = admin_client.patch(
        f'/user/{admin_user.pk}/',
        json.dumps({'email': 'foo@bar.com', 'version': initial_version}),
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == 'foo@bar.com'

    response = admin_client.patch(
        f'/user/{admin_user.pk}/',
        json.dumps({'email': 'foo@bar.com', 'version': initial_version}),
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.data == {
        'detail': 'RecordModifiedError: Record has been modified',
        'status_code': 409,
    }


@pytest.mark.django_db()
def test_get_serializer(client):
    """Testing UserViewSet.get_serializer with wrong parameters."""
    view_set = UserViewSet()
    view_set.request = mock.Mock
    invoker = User()
    view_set.request.user = invoker
    view_set.action = None
    view_set.format_kwarg = None

    # occurs only when rendering html form by calling /user/1/ from browser (not ajax)
    with pytest.raises(ValidationError, match='Permission error.'):
        view_set.get_serializer(instance=invoker)

    # action None should fail
    with pytest.raises(ValidationError, match='Permission error.'):
        view_set.get_serializer()

    invoker = auth.get_user(client)
    view_set.request.user = invoker
    view_set.permission_classes = [AllowAny]
    assert isinstance(view_set.get_serializer(), UserSerializerBase)
