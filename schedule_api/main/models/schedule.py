# -*- coding: utf-8 -*-
from schedule_api.lib.base_mixin import BaseMixin
from django.db import models


class Schedule(BaseMixin):
    """Model to store info about one day schedule."""

    class EducationFormat:
        FULL_TIME = 'Full-time'
        PART_TIME = 'Part-time'
        PART_TIME_EXPRESS = 'Part-time-express'
        formats = (
            FULL_TIME,
            PART_TIME,
            PART_TIME_EXPRESS,
        )
        choices = (
            (FULL_TIME, FULL_TIME),
            (PART_TIME, PART_TIME),
            (PART_TIME_EXPRESS, PART_TIME_EXPRESS),
        )

    title = models.CharField(max_length=200)
    faculty = models.CharField(max_length=500)
    year = models.IntegerField()
    term = models.IntegerField()
    education_format = models.CharField(
        max_length=20, choices=EducationFormat.choices, default=EducationFormat.FULL_TIME
    )

    def __str__(self):
        return self.title
