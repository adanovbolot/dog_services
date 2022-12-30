from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from main import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('services.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
