from rest_framework import viewsets, mixins, exceptions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from schedule_api.main.models import User
from schedule_api.main.permissions import IsUserOrReadOnly
from schedule_api.main.logic.user_base_serializer import (
    UserSerializerBase,
    UserCreate,
    UserList,
    UserUpdate,
)


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializerBase
    permission_classes = (IsUserOrReadOnly,)

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

        # serializer_class = super().get_serializer_class()
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
