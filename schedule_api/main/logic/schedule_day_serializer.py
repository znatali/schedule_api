# -*- coding: utf-8 -*-
from rest_framework import serializers
from schedule_api.main.models.schedule_day import ScheduleDay


class ScheduleDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = ScheduleDay
        fields = ('id', 'title', 'date', 'schedule')
