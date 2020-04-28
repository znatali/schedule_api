# -*- coding: utf-8 -*-
from rest_framework import serializers
from schedule_api.main.models.schedule_item import ScheduleItem


class ScheduleItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScheduleItem
        fields = ('id', 'title', 'start_time', 'end_time', 'type', 'teacher', 'sub_teacher', 'schedule_day')
