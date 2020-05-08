# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from server.apps.main.models.schedule_item import ScheduleItem


class ScheduleItemSerializer(serializers.ModelSerializer):
    """ScheduleItem Serializer."""

    class Meta(object):
        model = ScheduleItem
        fields = ('id', 'title', 'start_time', 'end_time', 'type', 'teacher', 'sub_teacher', 'schedule_day', 'version')

    @classmethod
    def validate_start_over_end(cls, new_start_time, new_end_time) -> ValidationError:
        """Validate start time over end time."""
        if new_start_time >= new_end_time:
            raise ValidationError(detail={
                'start_time': ['Start time cannot be later or equal then end time.'],
            })

    @classmethod
    def validate_over_time(cls, other_items, new_start_time, new_end_time) -> ValidationError:
        """Validate start time, end time logic."""
        for item in other_items:
            if new_start_time == item.start_time:
                raise ValidationError(detail={
                    'start_time': ['There is a class at this time already.'],
                })
            if item.start_time < new_start_time < item.end_time:
                raise ValidationError(detail={
                    'end_time': ['There is a class at this time already.'],
                })
            if new_end_time == item.end_time:
                raise ValidationError(detail={
                    'end_time': ['There is a class at this time already.'],
                })
            if new_start_time < item.start_time < new_end_time:
                raise ValidationError(detail={
                    'start_time': ['There is a class at this time already.'],
                })


class ScheduleItemCreateSerializer(ScheduleItemSerializer):
    """ScheduleItemCreate Serializer."""

    def validate(self, data):
        """Validates logic."""
        super().validate(data)
        new_start_time = data['start_time']
        new_end_time = data['end_time']
        ScheduleItemSerializer.validate_start_over_end(new_start_time, new_end_time)

        other_items = ScheduleItem.objects.filter(
            schedule_day=data['schedule_day'],
        )

        if other_items:
            ScheduleItemSerializer.validate_over_time(other_items, new_start_time, new_end_time)
        return data


class ScheduleItemUpdateSerializer(ScheduleItemSerializer):
    """ScheduleItemUpdate Serializer."""

    def validate(self, data):
        """Validates logic."""
        super().validate(data)
        start_time = self.instance.start_time
        end_time = self.instance.end_time
        if 'start_time' in data:
            start_time = data['start_time']
        if 'end_time' in data:
            end_time = data['end_time']
        ScheduleItemSerializer.validate_start_over_end(start_time, end_time)

        schedule_day_ref = self.instance.schedule_day
        if 'schedule_day' in data:
            schedule_day_ref = data['schedule_day']

        other_items = ScheduleItem.objects.filter(
            schedule_day=schedule_day_ref,
        ).exclude(id=self.instance.id)

        if other_items:
            ScheduleItemSerializer.validate_over_time(other_items, start_time, end_time)
        return data
