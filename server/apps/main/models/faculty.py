# -*- coding: utf-8 -*-
from django.db import models

from server.lib.base_mixin import BaseMixin

FACULTY_NAME_LONG_MAX = 300


class Faculty(BaseMixin):
    """Model to store info about faculty."""

    title = models.CharField(max_length=FACULTY_NAME_LONG_MAX)
    active = models.BooleanField(default=True)

    def __str__(self):
        """Return string self title."""
        return self.title
