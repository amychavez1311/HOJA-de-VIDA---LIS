from django.contrib import admin
from django.urls import path, include # Importante el include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Esta línea es la que debe ir para conectar con tu app
    path('', include('cv.urls')), 
]

# Esto permite ver las fotos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)