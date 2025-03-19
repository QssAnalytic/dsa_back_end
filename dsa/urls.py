from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]

# Serve media files in development or for testing with DEBUG=False
if settings.DEBUG or not settings.DEBUG:  # Temporary for testing
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
