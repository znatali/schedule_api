# -*- coding: utf-8 -*-
from schedule_api.lib.base_mixin import BaseMixin
from django.db import models


class ScheduleDay(BaseMixin):
    """Model to store info about one day schedule."""

    title = models.CharField(max_length=200)
    date = models.DateField()
    schedule = models.ForeignKey('Schedule', on_delete=models.PROTECT)

    def __str__(self):
        return self.title
