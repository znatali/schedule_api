from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from rest_framework import mixins, viewsets
from rest_framework.decorators import action

from server.apps.main.logic.schedule_day_serializer import ScheduleDaySerializer
from server.apps.main.logic.schedule_item_serializer import (
    ScheduleItemSerializer,
)
from server.apps.main.logic.schedule_serializer import ScheduleSerializer
from server.apps.main.models.schedule import Schedule
from server.apps.main.models.schedule_day import ScheduleDay
from server.apps.main.models.schedule_item import ScheduleItem


class ScheduleViewSet(mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Updates and retrieves schedules."""

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    @action(detail=True, methods=['get'])
    def download(self, request, pk):
        """Get formatted schedule."""

        wb = Workbook()
        ws = wb.active

        schedule = self.get_object()
        ws['A1'] = schedule.title
        ws['A2'] = schedule.faculty
        ws['A3'] = f'{str(schedule.year)} Курс'
        ws['A4'] = f'{str(schedule.term)} Семестр'
        ws['A5'] = schedule.education_format
        schedule_days = ScheduleDay.objects.filter(schedule=schedule).all()
        start_day_row = 6
        for schedule_day in schedule_days:
            ws.cell(row=start_day_row, column=1).value = f'{schedule_day.title} ' +\
                f'{schedule_day.date.strftime("%d-%b-%Y")}'
            schedule_items = ScheduleItem.objects.filter(schedule_day=schedule_day).all()
            start_day_row += 1
            for schedule_item in schedule_items:
                ws.cell(row=start_day_row, column=1).value = \
                    f'{schedule_item.start_time.strftime("%H:%M")} - ' \
                    + f'{schedule_item.end_time.strftime("%H:%M")}'
                ws.cell(row=start_day_row, column=2).value = f'{schedule_item.title} ({schedule_item.type})'
                ws.cell(row=start_day_row, column=3).value = schedule_item.teacher.get_full_name()
                start_day_row += 1

        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=sample.xlsx'
        return response


class ScheduleDayViewSet(mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Updates and retrieves schedules for a day."""
    queryset = ScheduleDay.objects.all()
    serializer_class = ScheduleDaySerializer


class ScheduleItemViewSet(mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Updates and retrieves schedule items."""
    queryset = ScheduleItem.objects.all()
    serializer_class = ScheduleItemSerializer
