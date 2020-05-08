# -*- coding: utf-8 -*-

import json
from unittest import mock

import pytest
from django.contrib import auth
from rest_framework import status
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.permissions import AllowAny

from server.apps.main.logic.schedule_item_serializer import (
    ScheduleItemSerializer,
)
from server.apps.main.models.schedule import Schedule
from server.apps.main.models.schedule_day import ScheduleDay
from server.apps.main.models.schedule_item import ScheduleItem
from server.apps.main.models.user import User
from server.apps.main.views.schedule import ScheduleItemViewSet

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
        'status_code': 400,
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

    # Create should fail because incorrect time.
    response = admin_client.post(
        '/schedule-item/',
        {
            'title': TEST_TITLE,
            'start_time': end_time,
            'end_time': start_time,
            'type': TEST_TYPE,
            'teacher': teacher_id,
            'schedule': schedule_id,
            'schedule_day': schedule_day_id,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        'start_time': [ErrorDetail(string='Start time cannot be later or equal then end time.', code='invalid')],
        'status_code': 400,
    }

    # Create should fail because incorrect time.
    response = admin_client.post(
        '/schedule-item/',
        {
            'title': TEST_TITLE,
            'start_time': end_time,
            'end_time': end_time,
            'type': TEST_TYPE,
            'teacher': teacher_id,
            'schedule': schedule_id,
            'schedule_day': schedule_day_id,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        'start_time': [ErrorDetail(string='Start time cannot be later or equal then end time.', code='invalid')],
        'status_code': 400,
    }

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
    assert response.data['start_time'] == start_time
    assert response.data['end_time'] == end_time

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

    # Update should fail because incorrect time.
    response = admin_client.patch(
        f'/schedule-item/{schedule_item_model.pk}/',
        json.dumps({
            'start_time': end_time,
            'end_time': end_time,
        }),
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        'start_time': [ErrorDetail(string='Start time cannot be later or equal then end time.', code='invalid')],
        'status_code': 400,
    }

    # Update schedule_day
    day_date_two = '2016-09-21'
    schedule_model = Schedule.objects.get(id=schedule_id)
    schedule_day_two = ScheduleDay.objects.create(
        title='Tuesday',
        date=day_date_two,
        schedule=schedule_model,
    )
    response = admin_client.patch(
        f'/schedule-item/{schedule_item_model.pk}/',
        json.dumps({
            'schedule_day': schedule_day_two.pk,
        }),
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data['schedule_day'] == schedule_day_two.pk

    # Create one more schedule_item, should fail because of same time
    response = admin_client.post(
        '/schedule-item/',
        {
            'title': TEST_TITLE,
            'start_time': start_time,
            'end_time': end_time,
            'type': TEST_TYPE,
            'teacher': teacher_id,
            'schedule': schedule_id,
            'schedule_day': schedule_day_two.pk,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        'start_time': [ErrorDetail(string='There is a class at this time already.', code='invalid')],
        'status_code': 400,
    }

    start_time_two = '07:30:00'
    response = admin_client.post(
        '/schedule-item/',
        {
            'title': TEST_TITLE,
            'start_time': start_time_two,
            'end_time': end_time,
            'type': TEST_TYPE,
            'teacher': teacher_id,
            'schedule': schedule_id,
            'schedule_day': schedule_day_two.pk,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        'end_time': [ErrorDetail(string='There is a class at this time already.', code='invalid')],
        'status_code': 400,
    }

    start_time_two = '09:45:00'
    response = admin_client.post(
        '/schedule-item/',
        {
            'title': TEST_TITLE,
            'start_time': start_time_two,
            'end_time': end_time,
            'type': TEST_TYPE,
            'teacher': teacher_id,
            'schedule': schedule_id,
            'schedule_day': schedule_day_two.pk,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        'start_time': [ErrorDetail(string='Start time cannot be later or equal then end time.', code='invalid')],
        'status_code': 400,
    }
    end_time_two = '11:30:00'
    response = admin_client.post(
        '/schedule-item/',
        {
            'title': TEST_TITLE,
            'start_time': start_time_two,
            'end_time': end_time_two,
            'type': TEST_TYPE,
            'teacher': teacher_id,
            'schedule': schedule_id,
            'schedule_day': schedule_day_two.pk,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert ScheduleItem.objects.count() == 2
    schedule_item_model_two_id = response.data['id']

    # Update should fail because incorrect time.
    response = admin_client.patch(
        f'/schedule-item/{schedule_item_model_two_id}/',
        json.dumps({
            'start_time': start_time,
        }),
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        'start_time': [ErrorDetail(string='There is a class at this time already.', code='invalid')],
        'status_code': 400,
    }

    # Update should fail because incorrect time.
    start_time_two = '08:45:00'
    response = admin_client.patch(
        f'/schedule-item/{schedule_item_model_two_id}/',
        json.dumps({
            'start_time': start_time_two,
        }),
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        'end_time': [ErrorDetail(string='There is a class at this time already.', code='invalid')],
        'status_code': 400,
    }

    # Update should fail because incorrect time.
    start_time_two = '07:45:00'
    end_time_two = '09:05:00'
    response = admin_client.patch(
        f'/schedule-item/{schedule_item_model_two_id}/',
        json.dumps({
            'start_time': start_time_two,
            'end_time': end_time_two,
        }),
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        'start_time': [ErrorDetail(string='There is a class at this time already.', code='invalid')],
        'status_code': 400,
    }

    # List should be successful.
    response = admin_client.get('/schedule-item/')
    assert response.status_code == status.HTTP_200_OK

    # Test download file schedule
    response = admin_client.get(f'/schedule/{schedule_id}/download/')
    assert response['Content-Disposition'] == f'attachment; filename=schedule.docx'
    assert response['Content-Type'] == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    assert len(response.content) > 0   # noqa: WPS507

    # Delete should be successful.
    response = admin_client.delete(
        f'/schedule-item/{schedule_item_model.pk}/',
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
def test_get_serializer(client):
    """Testing ScheduleItemViewSet.get_serializer with wrong parameters."""
    view_set = ScheduleItemViewSet()
    view_set.request = mock.Mock
    invoker = User()
    view_set.request.user = invoker
    view_set.action = None
    view_set.format_kwarg = None

    with pytest.raises(ValidationError, match='Permission error.'):
        view_set.get_serializer(instance=invoker)

    # action None should fail
    with pytest.raises(ValidationError, match='Permission error.'):
        view_set.get_serializer()

    invoker = auth.get_user(client)
    view_set.request.user = invoker
    view_set.permission_classes = [AllowAny]
    assert isinstance(view_set.get_serializer(), ScheduleItemSerializer)
