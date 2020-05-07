from rest_framework import mixins, permissions, viewsets

from server.apps.main.logic.faculty_serializer import FacultySerializer
from server.apps.main.models.faculty import Faculty


class FacultyViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Updates and retrieves faculty."""

    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = (permissions.IsAuthenticated,)
