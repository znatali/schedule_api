# -*- coding: utf-8 -*-
from rest_framework import serializers

from server.apps.main.models.schedule_item import ScheduleItem


class ScheduleItemSerializer(serializers.ModelSerializer):
    """ScheduleItem Serializer."""

    class Meta(object):
        model = ScheduleItem
        fields = ('id', 'title', 'start_time', 'end_time', 'type', 'teacher', 'sub_teacher', 'schedule_day', 'version')
