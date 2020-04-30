# -*- coding: utf-8 -*-
from django.db import models

from server.lib.base_mixin import BaseMixin

MAX_TITLE_LONG = 200
MAX_FORMAT_LONG = 20
MAX_FACULTY_LONG = 500


class Schedule(BaseMixin):
    """Model to store info about one day schedule."""

    class EducationFormat(object):
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

    title = models.CharField(max_length=MAX_TITLE_LONG)
    faculty = models.CharField(max_length=MAX_FACULTY_LONG)
    year = models.IntegerField()
    term = models.IntegerField()
    education_format = models.CharField(
        max_length=MAX_FORMAT_LONG, choices=EducationFormat.choices, default=EducationFormat.FULL_TIME,
    )

    def __str__(self):
        """Return string self title."""
        return self.title
