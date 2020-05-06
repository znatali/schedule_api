# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from server.apps.main.models.faculty import Faculty
from server.apps.main.models.schedule import Schedule
from server.apps.main.models.schedule_day import ScheduleDay
from server.apps.main.models.schedule_item import ScheduleItem
from server.apps.main.models.teacher import Teacher
from server.apps.main.models.user import User


@admin.register(User)
class UserProjectAdmin(UserAdmin):
    """Simple User."""


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Simple admin for Teacher."""

    list_display = (
        'id', 'first_name', 'middle_name', 'last_name', 'teaching_subject', 'created', 'modified', 'version',
    )


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    """Simple admin for Faculty."""

    list_display = ('id', 'title', 'active', 'created', 'modified', 'version')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """Simple admin for Schedule."""

    list_display = ('id', 'title', 'faculty', 'year', 'term', 'education_format', 'created', 'modified', 'version')


@admin.register(ScheduleDay)
class ScheduleDayAdmin(admin.ModelAdmin):
    """Simple admin for ScheduleDay."""

    list_display = ('id', 'title', 'date', 'created', 'modified', 'version')


@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    """Simple admin for ScheduleItem."""

    list_display = ('id', 'title', 'start_time', 'end_time', 'type', 'created', 'modified', 'version')
