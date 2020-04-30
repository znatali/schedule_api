# -*- coding: utf-8 -*-
from django.db import models

from server.lib.base_mixin import BaseMixin

MAX_TITLE_LONG = 200


class ScheduleDay(BaseMixin):
    """Model to store info about one day schedule."""

    title = models.CharField(max_length=MAX_TITLE_LONG)
    date = models.DateField()
    schedule = models.ForeignKey('Schedule', on_delete=models.PROTECT)

    def __str__(self):
        """Return string self title."""
        return self.title
