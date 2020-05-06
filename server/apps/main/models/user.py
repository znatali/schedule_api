# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser

from server.lib.base_mixin import BaseMixin


class User(BaseMixin, AbstractUser):
    """Extend django user with extra optional fields."""

    def __str__(self):
        """Return string self username."""
        return self.username
