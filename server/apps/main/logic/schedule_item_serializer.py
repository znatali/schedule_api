# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from server.apps.main.models.schedule_item import ScheduleItem


class ScheduleItemSerializer(serializers.ModelSerializer):
    """ScheduleItem Serializer."""

    class Meta(object):
        model = ScheduleItem
        fields = ('id', 'title', 'start_time', 'end_time', 'type', 'teacher', 'sub_teacher', 'schedule_day', 'version')

    def validate(self, data):  # noqa: C901
        """Validates logic."""
        super().validate(data)
        if 'start_time' in data and 'end_time' in data:
            if data['start_time'] > data['end_time']:
                raise ValidationError(detail={
                    'start_time': ['Start time cannot be later then end time.'],
                })
        if 'schedule_day' in data:
            other_items = ScheduleItem.objects.filter(
                schedule_day=data['schedule_day'],
            )
        else:
            other_items = ScheduleItem.objects.filter(
                schedule_day=self.instance.schedule_day,
            )
        if self.instance:
            other_items = other_items.exclude(id=self.instance.id)

        if other_items:
            for item in other_items:
                if 'start_time' in data:
                    if data['start_time'] == item.start_time:
                        raise ValidationError(detail={
                            'start_time': ['There is a class at this time already.'],
                        })
                    if item.start_time < data['start_time'] < item.end_time:
                        raise ValidationError(detail={
                            'end_time': ['There is a class at this time already.'],
                        })
                if 'end_time' in data and data['end_time'] == item.end_time:
                    raise ValidationError(detail={
                        'end_time': ['There is a class at this time already.'],
                    })
                if 'start_time' in data and 'end_time' in data:
                    if data['start_time'] < item.start_time < data['end_time']:
                        raise ValidationError(detail={
                            'start_time': ['There is a class at this time already.'],
                        })
        return data
