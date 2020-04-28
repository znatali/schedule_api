from rest_framework import viewsets, mixins
from schedule_api.main.models.teacher import Teacher
from schedule_api.main.logic.teacher_serializer import TeacherSerializer


class TeacherViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    Updates and retrieves teachers
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
