# -*- coding: utf-8 -*-
from schedule_api.lib.base_mixin import BaseMixin
from django.contrib.postgres.fields import JSONField
from django.db import models


class Teacher(BaseMixin):
    """Model to store info about teacher."""

    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    teaching_subject = JSONField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name

    def get_full_name(self):
        return self.first_name + ' ' + self.middle_name + ' ' + self.last_name
