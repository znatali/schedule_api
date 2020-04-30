
"""
Main URL mapping configuration file.

Include other URLConfs from external apps using method `include()`.

It is also a good practice to keep a single URL to the root index page.

This examples uses Django's default media
files serving technique in development.
"""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls
from django.urls import path
from django.views.generic import TemplateView

from server.apps.main import urls as main_urls

admin.autodiscover()


urlpatterns = [
    # Apps:
    url(r'^', include(main_urls, namespace='main')),

    # Health checks:
    url(r'^health/', include('health_check.urls')),  # noqa: DJ05

    # django-admin:
    url('admin/doc/', include(admindocs_urls)),  # noqa: DJ05
    url('admin/', admin.site.urls),

    # Text and xml static files:
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name='txt/robots.txt',
        content_type='text/plain',
    )),
    url(r'^humans\.txt$', TemplateView.as_view(
        template_name='txt/humans.txt',
        content_type='text/plain',
    )),
]

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar  # noqa: WPS433
    from django.conf.urls.static import static  # noqa: WPS433

    urlpatterns = [
        # URLs specific only to django-debug-toolbar:
        path('__debug__/', include(debug_toolbar.urls)),  # noqa: DJ05
    ] + urlpatterns + static(
        # Serving media files in development only:
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

admin.autodiscover()
