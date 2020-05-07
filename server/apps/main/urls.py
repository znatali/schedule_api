from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from server.apps.main.views.faculty import FacultyViewSet
from server.apps.main.views.index import index
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
router.register(r'teacher', TeacherViewSet)
router.register(r'schedule', ScheduleViewSet)
router.register(r'schedule-day', ScheduleDayViewSet)
router.register(r'schedule-item', ScheduleItemViewSet)
router.register(r'faculty', FacultyViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('hello', index, name='hello'),
    url(r'^', include((router.urls, app_name), namespace='drf'), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
