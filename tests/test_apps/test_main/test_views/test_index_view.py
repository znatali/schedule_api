# -*- coding: utf-8 -*-

from rest_framework import status


def test_main_page(client, main_heading):
    """This test ensures that main page works."""
    response = client.get('/hello')

    assert response.status_code == 200


def test_admin(admin_client, admin_user):
    """Make sure Admin works for User."""
    response = admin_client.get('/admin/main/user/')
    assert response.status_code == status.HTTP_200_OK

    response = admin_client.get(f'/admin/main/user/{admin_user.pk}/change/')
    assert response.status_code == status.HTTP_200_OK
