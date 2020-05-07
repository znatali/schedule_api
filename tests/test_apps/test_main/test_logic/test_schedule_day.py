# -*- coding: utf-8 -*-

import json

from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from server.apps.main.models.schedule_day import ScheduleDay

TEST_SCHEDULE_TITLE = 'Schedule1'
TEST_YEAR = 1
TEST_TERM = 1
TEST_FORMAT = 'Full-time'
TEST_TITLE = 'Monday'


def test_schedule_day(admin_client, admin_user):
    """Create ScheduleDay."""
    # Create without schedule should fail.
    day_date = '2016-09-20'
    response = admin_client.post(
        '/schedule-day/',
        {
            'title': TEST_TITLE,
            'date': day_date,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {'schedule': [ErrorDetail(string='This field is required.', code='required')]}

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

    # Create schedule day should be successful.
    response = admin_client.post(
        '/schedule-day/',
        {
            'title': TEST_TITLE,
            'date': day_date,
            'schedule': response.data['id'],
        },
    )
    assert response.status_code == status.HTTP_201_CREATED

    schedule_day_model = ScheduleDay.objects.get(id=response.data['id'])
    assert len(str(schedule_day_model)) <= 20

    response = admin_client.patch(
        f'/schedule-day/{schedule_day_model.pk}/',
        json.dumps({
            'title': f'{TEST_TITLE}_{TEST_TITLE}',
        }),
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == f'{TEST_TITLE}_{TEST_TITLE}'

    # Delete should be successful.
    response = admin_client.delete(
        f'/schedule-day/{schedule_day_model.pk}/',
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
