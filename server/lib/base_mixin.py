# -*- coding: utf-8 -*-

from concurrency.fields import IntegerVersionField
from django.db import models


class BaseMixin(models.Model):
    """Base fields: created, modified, version."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    version = IntegerVersionField()

    class Meta(object):
        abstract = True

    def __str__(self):
        """Return string self id."""
        return str(self.pk)
