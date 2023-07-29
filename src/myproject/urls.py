from django.conf import settings
from django.urls import path, include
from django.urls.conf import re_path
from base.views import DocumentUploadS3ApiView
from base.views import health_check
from django.conf import settings
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from myproject.settings import STATIC_ROOT, STATIC_URL

schema_view = get_schema_view(
    openapi.Info(
        title=settings.PROJECT_TITLE,
        default_version=settings.PROJECT_VERSION,
        description="Api description",
        contact=openapi.Contact(email="mahmudul.hassan240@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=(permissions.IsAuthenticated,),
)

v1_patterns = [
    path('accounts/', include('accounts.urls', namespace='accounts.apis')),
]

urlpatterns = [
    path('', health_check),
    path('api/', include([
        path('v1.0/', include(v1_patterns))
    ])),
    path('admin/', admin.site.urls),
    path('s3-upload/', DocumentUploadS3ApiView.as_view()),
]

urlpatterns += [path('api-auth/', include('rest_framework.urls')), ]

urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
# urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$',
                schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger',
                cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc',
                cache_timeout=0), name='schema-redoc'),
    ]
