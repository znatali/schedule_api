from rest_framework import mixins, permissions, viewsets

from server.apps.main.logic.teacher_serializer import TeacherSerializer
from server.apps.main.models.teacher import Teacher


class TeacherViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Updates and retrieves teachers."""

    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (permissions.IsAuthenticated,)
