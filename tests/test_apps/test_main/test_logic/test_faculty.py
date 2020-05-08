# -*- coding: utf-8 -*-

import json

from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from server.apps.main.models.faculty import FACULTY_NAME_LONG_MAX, Faculty

TEST_TITLE = 'Science'


def test_faculty(admin_client, admin_user):
    """Create Faculty."""
    # Create with long title should fail.
    response = admin_client.post(
        '/faculty/',
        {
            'title': TEST_TITLE * 100,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        'title': [
            ErrorDetail(
                string=f'Ensure this field has no more than {FACULTY_NAME_LONG_MAX} characters.',
                code='max_length',
            ),
        ],
        'status_code': 400,
    }

    # Create should be successful.
    response = admin_client.post(
        '/faculty/',
        {
            'title': TEST_TITLE,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Update should be successful.
    faculty = Faculty.objects.get(id=response.data['id'])
    response = admin_client.patch(
        f'/faculty/{faculty.pk}/',
        json.dumps({
            'title': f'{TEST_TITLE}_{TEST_TITLE}',
        }),
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == f'{TEST_TITLE}_{TEST_TITLE}'

    # Delete should be successful.
    response = admin_client.delete(
        f'/faculty/{faculty.pk}/',
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
