# -*- coding: utf-8 -*-
from typing import List

from rest_framework import serializers
from schedule_api.main.models.user import User


class UserSerializerBase(serializers.ModelSerializer):

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
        ]
        read_only_fields: List[str] = ['created', 'modified']


class UserList(UserSerializerBase):
    """List any users Serializer."""

    class Meta(UserSerializerBase.Meta):
        fields = UserSerializerBase.Meta.fields + ['username']


class UserCreate(UserSerializerBase):
    """Create a user Serializer."""

    class Meta(UserSerializerBase.Meta):
        fields = UserSerializerBase.Meta.fields + ['username', 'first_name', 'last_name', 'auth_token', 'password']
        read_only_fields = ('auth_token',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # call create_user on user object.
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdate(UserSerializerBase):
    """Update a user Serializer."""

    class Meta(UserSerializerBase.Meta):
        fields = UserSerializerBase.Meta.fields + ['first_name', 'last_name', 'password']
        read_only_fields = ('auth_token',)
        extra_kwargs = {'password': {'write_only': True}}
