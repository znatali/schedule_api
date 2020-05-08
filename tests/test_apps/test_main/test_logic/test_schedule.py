# -*- coding: utf-8 -*-

import json

from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from server.apps.main.models.schedule import Schedule

TEST_TITLE = 'Schedule1'
TEST_YEAR = 1
TEST_TERM = 1
TEST_FORMAT = 'Full-time'


def test_schedule(admin_client, admin_user):
    """Create Schedule."""
    # Create without faculty should fail.
    response = admin_client.post(
        '/schedule/',
        {
            'title': TEST_TITLE,
            'year': TEST_YEAR,
            'term': TEST_TERM,
            'education_format': TEST_FORMAT,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        'faculty': [ErrorDetail(string='This field is required.', code='required')],
        'status_code': 400,
    }

    # Create faculty first, then create schedule should be successful.
    response = admin_client.post(
        '/faculty/',
        {
            'title': TEST_TITLE,
        },
    )

    response = admin_client.post(
        '/schedule/',
        {
            'title': TEST_TITLE,
            'year': TEST_YEAR,
            'term': TEST_TERM,
            'faculty': response.data['id'],
            'education_format': TEST_FORMAT,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED

    schedule_model = Schedule.objects.get(id=response.data['id'])
    assert len(str(schedule_model)) <= 20

    response = admin_client.patch(
        f'/schedule/{schedule_model.pk}/',
        json.dumps({
            'title': f'{TEST_TITLE}_{TEST_TITLE}',
        }),
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == f'{TEST_TITLE}_{TEST_TITLE}'

    # Delete should be successful.
    response = admin_client.delete(
        f'/schedule/{schedule_model.pk}/',
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
