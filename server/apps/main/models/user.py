# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from server.lib.base_mixin import BaseMixin


class User(BaseMixin, AbstractUser):
    """Extend django user with extra optional fields."""

    def __str__(self):
        """Return string self username."""
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Create auth token."""
    if created:
        Token.objects.create(user=instance)
