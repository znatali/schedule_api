from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path, reverse_lazy
from django.views.generic.base import RedirectView
from rest_framework import routers
from rest_framework.authtoken import views

from server.apps.main.views.auth import AuthViewSet
from server.apps.main.views.schedule import (
    ScheduleDayViewSet,
    ScheduleItemViewSet,
    ScheduleViewSet,
)
from server.apps.main.views.teacher import TeacherViewSet
from server.apps.main.views.user import UserViewSet

app_name = 'main'

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'rest-auth', AuthViewSet, basename='rest-auth')
router.register(r'teacher', TeacherViewSet)
router.register(r'schedule', ScheduleViewSet)
router.register(r'schedule-day', ScheduleDayViewSet)
router.register(r'schedule-item', ScheduleItemViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    url(r'^', include((router.urls, app_name), namespace='drf'), name='index'),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
