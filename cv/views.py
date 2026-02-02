from django.shortcuts import render
from .models import (
    Perfil,
    Educacion,
    Experiencia,
    Habilidad,
    Referencia,
    VentaGarage
)

def home(request):
    """ Vista de la 'Gran Puerta' de entrada """
    perfil = Perfil.objects.first()
    
    # Verificamos si hay productos para mostrar el botón de la tienda en el Home
    ventas_disponibles = VentaGarage.objects.filter(disponible=True)
    
    context = {
        'perfil': perfil,
        'proyectos': perfil.proyectos.all()[:3] if perfil else [],
        'habilidades': Habilidad.objects.all()[:6],
        'hay_productos': ventas_disponibles.exists(), # Para el botón del Home
    }
    
    return render(request, 'cv/home.html', context)


def cv_view(request):
    """ Vista detallada de la Hoja de Vida """
    perfil = Perfil.objects.first()

    context = {
        'perfil': perfil,

        # Listados generales
        'educaciones': Educacion.objects.all(),
        'experiencias': Experiencia.objects.all(),
        'habilidades': Habilidad.objects.all(),
        'referencias': Referencia.objects.all(),

        # Relacionados al perfil
        'certificados': perfil.certificados.all() if perfil else [],
        'proyectos': perfil.proyectos.all() if perfil else [],

        # Para el botón pequeño de la tienda en el Navbar del CV
        'hay_productos': VentaGarage.objects.filter(disponible=True).exists()
    }

    return render(request, 'cv/cv.html', context)


def tienda_view(request):
    """ Vista independiente para la Venta de Garage """
    perfil = Perfil.objects.first()
    productos = VentaGarage.objects.filter(disponible=True).order_by('-fecha_publicacion')
    
    context = {
        'perfil': perfil,
        'productos': productos,
    }
    
    return render(request, 'cv/tienda.html', context)