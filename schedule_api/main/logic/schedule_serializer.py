# -*- coding: utf-8 -*-
from rest_framework import serializers
from schedule_api.main.models.schedule import Schedule


class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ('id', 'title', 'faculty', 'year', 'term', 'education_format',)
