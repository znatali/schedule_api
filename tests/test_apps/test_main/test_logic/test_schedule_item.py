# -*- coding: utf-8 -*-

import json

from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from server.apps.main.models.schedule_item import ScheduleItem

TEST_SCHEDULE_TITLE = 'Schedule1'
TEST_YEAR = 1
TEST_TERM = 1
TEST_FORMAT = 'Full-time'

TEST_TITLE = 'Monday'
TEST_TYPE = 'Exam'

TEST_FIRST_NAME = 'John'
TEST_LAST_NAME = 'Smith'
TEST_MIDDLE_NAME = 'S'


def test_schedule_item(admin_client, admin_user):
    """Create ScheduleItem."""
    # Create without schedule_day, teacher should fail.
    day_date = '2016-09-20'
    start_time = '08:00:00'
    end_time = '09:35:00'
    response = admin_client.post(
        '/schedule-item/',
        {
            'title': TEST_TITLE,
            'start_time': start_time,
            'end_time': end_time,
            'type': TEST_TYPE,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        'schedule_day': [ErrorDetail(string='This field is required.', code='required')],
        'teacher': [ErrorDetail(string='This field is required.', code='required')],
    }

    # Create teacher, faculty, schedule, schedule_day first, then create schedule_item should be successful.
    response = admin_client.post(
        '/teacher/',
        {
            'first_name': TEST_FIRST_NAME,
            'last_name': TEST_LAST_NAME,
            'middle_name': TEST_MIDDLE_NAME,
        },
    )
    teacher_id = response.data['id']

    response = admin_client.post(
        '/faculty/',
        {
            'title': TEST_TITLE,
        },
    )
    faculty_id = response.data['id']

    response = admin_client.post(
        '/schedule/',
        {
            'title': TEST_TITLE,
            'year': TEST_YEAR,
            'term': TEST_TERM,
            'faculty': faculty_id,
            'education_format': TEST_FORMAT,
        },
    )
    schedule_id = response.data['id']

    response = admin_client.post(
        '/schedule-day/',
        {
            'title': TEST_TITLE,
            'date': day_date,
            'schedule': schedule_id,
        },
    )
    schedule_day_id = response.data['id']

    # Create should be successful.
    response = admin_client.post(
        '/schedule-item/',
        {
            'title': TEST_TITLE,
            'start_time': start_time,
            'end_time': end_time,
            'type': TEST_TYPE,
            'teacher': teacher_id,
            'schedule': schedule_id,
            'schedule_day': schedule_day_id,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Update should be successful.
    schedule_item_model = ScheduleItem.objects.get(id=response.data['id'])
    assert len(str(schedule_item_model)) <= 20

    response = admin_client.patch(
        f'/schedule-item/{schedule_item_model.pk}/',
        json.dumps({
            'title': f'{TEST_TITLE}_{TEST_TITLE}',
        }),
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == f'{TEST_TITLE}_{TEST_TITLE}'

    # Delete should be successful.
    response = admin_client.delete(
        f'/schedule-item/{schedule_item_model.pk}/',
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
