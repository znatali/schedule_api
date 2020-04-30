# -*- coding: utf-8 -*-
from rest_framework import serializers

from server.apps.main.models.schedule_day import ScheduleDay


class ScheduleDaySerializer(serializers.ModelSerializer):
    """ScheduleDay Serializer."""

    class Meta(object):
        model = ScheduleDay
        fields = ('id', 'title', 'date', 'schedule', 'version')
