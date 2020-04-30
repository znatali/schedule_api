# -*- coding: utf-8 -*-
from rest_framework import serializers

from server.apps.main.models.schedule import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    """Schedule model serializer."""

    class Meta(object):
        model = Schedule
        fields = ('id', 'title', 'faculty', 'year', 'term', 'education_format', 'version')
