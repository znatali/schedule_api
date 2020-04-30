# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from server.apps.main.logic.user_base_serializer import UserSerializerBase
from server.apps.main.models.user import User


def _auth(user: User):
    """Check user authentication and return it serialized."""
    if not user or not user.pk or not user.is_active:
        raise NotAuthenticated

    user_object = UserSerializerBase(user).data

    response = {
        'userObj': user_object,
    }
    return Response(response)


class LoginSerializer(serializers.Serializer):
    """Using in auth.login."""

    password = serializers.CharField(max_length=100)
    username = serializers.CharField()


def internal_login(request, username: str, password: str):
    """Login and auth response."""
    auth_user = authenticate(username=username, password=password, request=request)
    response = _auth(auth_user)
    django_login(request, auth_user)
    return response


class AuthViewSet(ViewSet):
    """Auth API."""

    serializer_class = LoginSerializer  # does not affect to any logic
    permission_classes = [AllowAny]

    @action(detail=False, methods=['GET'])
    def auth(self, request):
        """First API call for frontend."""
        try:
            return _auth(request.user)
        except NotAuthenticated as exception:
            # auth should return stripe publicKey even on failure
            return Response(
                data={
                    'detail': exception.detail,
                    'status_code': status.HTTP_403_FORBIDDEN,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    @action(detail=False, methods=['POST'], serializer_class=LoginSerializer)
    def login(self, request):
        """Login and auth response."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return internal_login(
            request=request,
            username=request.data.get('username', ''),
            password=request.data.get('password', ''),
        )

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        """Logout user."""
        logout(request)
        return Response()
