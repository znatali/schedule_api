# -*- coding: utf-8 -*-
from django.db import models

from server.apps.main.models.teacher import Teacher
from server.lib.base_mixin import BaseMixin

MAX_TITLE_LONG = 200
MAX_TYPE_LONG = 20


class ScheduleItem(BaseMixin):
    """Model to store info about one lesson."""

    class Type(object):
        END_OF_TERM_TEST = 'End-of-term-test'
        TEST = 'Test'
        EXAM = 'Exam'
        LECTURE = 'Lecture'
        PRACTICE = 'Practice'
        types = (
            END_OF_TERM_TEST,
            TEST,
            EXAM,
            LECTURE,
            PRACTICE,
        )
        choices = (
            (END_OF_TERM_TEST, END_OF_TERM_TEST),
            (TEST, TEST),
            (EXAM, EXAM),
            (LECTURE, LECTURE),
            (PRACTICE, PRACTICE),
        )

    title = models.CharField(max_length=MAX_TITLE_LONG)
    start_time = models.TimeField()
    end_time = models.TimeField()
    type = models.CharField(max_length=MAX_TYPE_LONG, choices=Type.choices, default=Type.LECTURE)  # noqa: WPS125
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='item_teacher')
    sub_teacher = models.ForeignKey(
        Teacher, null=True, blank=True, on_delete=models.PROTECT, related_name='item_sub_teacher',
    )
    schedule_day = models.ForeignKey('ScheduleDay', on_delete=models.PROTECT)

    class Meta(object):
        constraints = [
            models.UniqueConstraint(
                fields=['start_time', 'schedule_day'],
                name='start_time_schedule_day',
            ),
            models.UniqueConstraint(
                fields=['end_time', 'schedule_day'],
                name='end_time_schedule_day',
            ),
            models.UniqueConstraint(
                fields=['title', 'start_time', 'schedule_day', 'teacher'],
                name='title_start_time_schedule_day_teacher',
            ),
            models.UniqueConstraint(
                fields=['title', 'end_time', 'schedule_day', 'teacher'],
                name='title_end_time_schedule_day_teacher',
            ),
        ]

    def __str__(self):
        """Return string self title."""
        return self.title
