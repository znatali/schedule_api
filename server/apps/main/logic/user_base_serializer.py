# -*- coding: utf-8 -*-
from typing import List

from rest_framework import serializers

from server.apps.main.models.user import User


class UserSerializerBase(serializers.ModelSerializer):
    """List any users Serializer."""

    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta(object):
        model = User
        fields: List[str] = [
            'created',
            'email',
            'first_name',
            'id',
            'last_name',
            'version',
        ]
        read_only_fields: List[str] = ['created', 'modified']


class UserList(UserSerializerBase):
    """List any users Serializer."""

    class Meta(UserSerializerBase.Meta):
        fields = UserSerializerBase.Meta.fields + ['username']


class UserCreate(UserSerializerBase):
    """Create a user Serializer."""

    class Meta(UserSerializerBase.Meta):
        fields = UserSerializerBase.Meta.fields + ['username', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserUpdate(UserSerializerBase):
    """Update a user Serializer."""

    class Meta(UserSerializerBase.Meta):
        fields = UserSerializerBase.Meta.fields + ['first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}
