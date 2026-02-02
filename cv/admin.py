from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Perfil, Educacion, Experiencia, Habilidad, 
    Certificado, Proyecto, Referencia, VentaGarage
)

def generar_miniatura(url):
    if url:
        return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px; object-fit: cover;" />', url)
    return "Sin imagen"

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("nombres", "apellidos", "profesion", "email", "cedula", "ver_foto")
    search_fields = ("nombres", "apellidos", "cedula", "email")
    fieldsets = (
        ('Información Personal', {'fields': (('nombres', 'apellidos'), 'foto', 'descripcion')}),
        ('Identificación', {'fields': ('cedula', 'fecha_nacimiento', 'nacionalidad', 'lugar_nacimiento')}),
        ('Contacto', {'fields': ('email', 'telefono', 'sitio_web', 'direccion_domiciliaria', 'direccion_trabajo')}),
        ('Otros', {'fields': ('sexo', 'estado_civil', 'licencia_conducir', 'profesion')}),
    )
    def ver_foto(self, obj): return generar_miniatura(obj.foto.url if obj.foto else None)

@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ("nombre_producto", "precio", "estado", "disponible", "ver_miniatura")
    list_filter = ("estado", "disponible")
    def ver_miniatura(self, obj): return generar_miniatura(obj.imagen.url if obj.imagen else None)

@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "institucion", "fecha", "ver_archivo")
    def ver_archivo(self, obj): return generar_miniatura(obj.imagen.url if obj.imagen else None)

@admin.register(Educacion)
class EducacionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "institucion", "fecha_inicio", "fecha_fin", "ver_foto")
    def ver_foto(self, obj): return generar_miniatura(obj.foto_certificado.url if obj.foto_certificado else None)

@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ("cargo", "empresa", "fecha_inicio", "fecha_fin", "ver_foto")
    def ver_foto(self, obj): return generar_miniatura(obj.foto_evidencia.url if obj.foto_evidencia else None)

@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "nivel_estrellas")
    def nivel_estrellas(self, obj): return "⭐" * obj.nivel

admin.site.register(Proyecto)
admin.site.register(Referencia)