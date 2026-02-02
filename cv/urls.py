from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Ruta de la 'Gran Puerta' (Home)
    path('', views.home, name='home'),
    
    # Ruta de la Hoja de Vida detallada
    path('cv/', views.cv_view, name='cv'),
    
    # Nueva ruta para la Tienda / Venta de Garage independiente
    path('tienda/', views.tienda_view, name='tienda'),
]

# Esto permite que Django maneje los archivos multimedia durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)