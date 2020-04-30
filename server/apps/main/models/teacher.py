# -*- coding: utf-8 -*-
from django.contrib.postgres.fields import JSONField
from django.db import models

from server.lib.base_mixin import BaseMixin

TEACHER_NAME_LONG_MAX = 200


class Teacher(BaseMixin):
    """Model to store info about teacher."""

    first_name = models.CharField(max_length=TEACHER_NAME_LONG_MAX)
    middle_name = models.CharField(max_length=TEACHER_NAME_LONG_MAX)
    last_name = models.CharField(max_length=TEACHER_NAME_LONG_MAX)
    teaching_subject = JSONField()
    active = models.BooleanField(default=True)

    def __str__(self):
        """Return string self first_name."""
        return self.first_name

    def get_full_name(self):
        """Return full name."""
        return f'{self.first_name} {self.middle_name} {self.last_name}'
