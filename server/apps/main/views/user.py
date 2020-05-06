from rest_framework import exceptions, mixins, permissions, viewsets
from rest_framework.permissions import AllowAny

from server.apps.main.logic.user_base_serializer import (
    UserCreate,
    UserList,
    UserSerializerBase,
    UserUpdate,
)
from server.apps.main.models import User


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Updates and retrieves user accounts."""

    queryset = User.objects.all()
    serializer_class = UserSerializerBase
    permission_classes = (permissions.AllowAny,)

    def get_serializer(self, *args, **kwargs):
        """
        Route serializers based on action.

            list                    UserList
            retrieve                UserUpdate
            update, partial_update  UserUpdate
            create                  UserCreate
        """
        if self.request.user.is_anonymous and AllowAny in self.permission_classes:
            kwargs['context'] = self.get_serializer_context()
            return self.serializer_class(*args, **kwargs)
        if self.action == 'list':
            serializer_class = UserList
        elif self.action in {'update', 'partial_update', 'retrieve'}:
            serializer_class = UserUpdate
        elif self.action == 'create':
            serializer_class = UserCreate
        else:
            serializer_class = None

        if serializer_class is None:
            raise exceptions.ValidationError(detail={self.action: ['Permission error.']})
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
