# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from schedule_api.main.models.user import User
from schedule_api.main.models.teacher import Teacher
from schedule_api.main.models.schedule import Schedule
from schedule_api.main.models.schedule_day import ScheduleDay
from schedule_api.main.models.schedule_item import ScheduleItem


@admin.register(User)
class UserProjectAdmin(UserAdmin):
    pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Simple admin for Teacher."""

    list_display = ('id', 'first_name', 'middle_name', 'last_name', 'teaching_subject', 'created', 'modified')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """Simple admin for Schedule."""

    list_display = ('id', 'title', 'faculty', 'year', 'term', 'education_format', 'created', 'modified')


@admin.register(ScheduleDay)
class ScheduleDayAdmin(admin.ModelAdmin):
    """Simple admin for ScheduleDay."""

    list_display = ('id', 'title', 'date', 'created', 'modified')


@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    """Simple admin for ScheduleItem."""

    list_display = ('id', 'title', 'start_time', 'end_time', 'type', 'created', 'modified')
