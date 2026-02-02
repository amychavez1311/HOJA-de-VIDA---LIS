from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

# --- VALIDADORES ---
cedula_validator = RegexValidator(
    regex=r'^\d{10}$',
    message='La cédula debe contener exactamente 10 dígitos numéricos.'
)

def validar_no_futuro(value):
    if value > timezone.now().date():
        raise ValidationError('La fecha no puede ser una fecha futura.')

# --- MODELOS ---

class Perfil(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=50)
    lugar_nacimiento = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(validators=[validar_no_futuro])
    cedula = models.CharField(max_length=10, unique=True, validators=[cedula_validator])
    
    sexo = models.CharField(
        max_length=10,
        choices=[("Masculino", "Masculino"), ("Femenino", "Femenino"), ("Otro", "Otro")]
    )
    estado_civil = models.CharField(
        max_length=20,
        choices=[("Soltero", "Soltero"), ("Casado", "Casado"), ("Divorciado", "Divorciado"), ("Viudo", "Viudo")]
    )
    licencia_conducir = models.BooleanField(default=False)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    sitio_web = models.URLField(blank=True, null=True)
    direccion_domiciliaria = models.CharField(max_length=200)
    direccion_trabajo = models.CharField(max_length=200, blank=True, null=True)
    profesion = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to="proyecto_cv_v2/perfil/", blank=True, null=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Datos Personales"

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Educacion(models.Model):
    institucion = models.CharField(max_length=150)
    titulo = models.CharField(max_length=150)
    fecha_inicio = models.DateField(validators=[validar_no_futuro])
    fecha_fin = models.DateField(blank=True, null=True, validators=[validar_no_futuro])
    descripcion = models.TextField(blank=True)
    # Solución Error: No dejaba cargar foto en académicos/cursos
    foto_certificado = models.ImageField(upload_to="proyecto_cv_v2/educacion/", blank=True, null=True)

    def clean(self):
        if self.fecha_fin and self.fecha_inicio > self.fecha_fin:
            raise ValidationError({'fecha_inicio': 'La fecha de inicio no puede ser posterior a la de fin.'})

    class Meta:
        verbose_name = "Educación"
        verbose_name_plural = "Educación"

class Experiencia(models.Model):
    empresa = models.CharField(max_length=150)
    cargo = models.CharField(max_length=150)
    fecha_inicio = models.DateField(validators=[validar_no_futuro])
    fecha_fin = models.DateField(blank=True, null=True, validators=[validar_no_futuro])
    descripcion = models.TextField()
    # Solución Error: No dejaba cargar foto en productos laborales
    foto_evidencia = models.ImageField(upload_to="proyecto_cv_v2/experiencia/", blank=True, null=True)

    def clean(self):
        if self.fecha_fin and self.fecha_inicio > self.fecha_fin:
            raise ValidationError({'fecha_inicio': 'La fecha de inicio no puede ser posterior a la de fin.'})

    class Meta:
        verbose_name = "Experiencia"
        verbose_name_plural = "Experiencias"

class Habilidad(models.Model):
    nombre = models.CharField(max_length=100)
    nivel = models.IntegerField(help_text="Nivel del 1 al 5")

    class Meta:
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"

    def __str__(self):
        return self.nombre

class Certificado(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="certificados")
    titulo = models.CharField(max_length=200)
    institucion = models.CharField(max_length=200)
    fecha = models.DateField(validators=[validar_no_futuro])
    # Solución Error: No dejaba cargar foto en Reconocimientos
    imagen = models.ImageField(upload_to="proyecto_cv_v2/certificados/")

    class Meta:
        verbose_name = "Certificado/Reconocimiento"
        verbose_name_plural = "Certificados"

class Proyecto(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="proyectos")
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tecnologias = models.CharField(max_length=300)
    github = models.URLField(blank=True, null=True)
    demo = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

class Referencia(models.Model):
    nombre = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = "Referencia"
        verbose_name_plural = "Referencias"

class VentaGarage(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="ventas_garage")
    nombre_producto = models.CharField(max_length=150)
    descripcion = models.TextField()
    # Solución Error: Decimales incorrectos (50 -> 20,0000)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[("Nuevo", "Nuevo"), ("Usado", "Usado")])
    disponible = models.BooleanField(default=True)
    # Solución Error: No dejaba cargar foto
    imagen = models.ImageField(upload_to="proyecto_cv_v2/venta_garage/", blank=True, null=True)
    fecha_publicacion = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Venta de Garage"
        verbose_name_plural = "Artículos Venta de Garage"