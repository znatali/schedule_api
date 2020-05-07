# -*- coding: utf-8 -*-

import json

from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from server.apps.main.models.teacher import Teacher

TEST_FIRST_NAME = 'John'
TEST_LAST_NAME = 'Smith'
TEST_MIDDLE_NAME = 'S'


def test_teacher(admin_client, admin_user):
    """Create Teacher."""
    # Create without middle name should fail.
    response = admin_client.post(
        '/teacher/',
        {
            'first_name': TEST_FIRST_NAME,
            'last_name': TEST_LAST_NAME,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {'middle_name': [ErrorDetail(string='This field is required.', code='required')]}

    # Create should be successful.
    response = admin_client.post(
        '/teacher/',
        {
            'first_name': TEST_FIRST_NAME,
            'last_name': TEST_LAST_NAME,
            'middle_name': TEST_MIDDLE_NAME,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Update should be successful.
    teacher = Teacher.objects.get(id=response.data['id'])
    response = admin_client.patch(
        f'/teacher/{teacher.pk}/',
        json.dumps({
            'middle_name': f'{TEST_FIRST_NAME}',
        }),
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data['middle_name'] == f'{TEST_FIRST_NAME}'

    # Delete should be successful.
    response = admin_client.delete(
        f'/teacher/{teacher.pk}/',
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
