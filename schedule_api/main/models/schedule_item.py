# -*- coding: utf-8 -*-
from schedule_api.lib.base_mixin import BaseMixin
from django.db import models
from schedule_api.main.models.teacher import Teacher


class ScheduleItem(BaseMixin):
    """Model to store info about one lesson."""

    class Type:
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

    title = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.LECTURE)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='item_teacher')
    sub_teacher = models.ForeignKey(
        Teacher, null=True, blank=True, on_delete=models.PROTECT, related_name='item_sub_teacher'
    )
    schedule_day = models.ForeignKey('ScheduleDay', on_delete=models.PROTECT)

    def __str__(self):
        return self.title
