from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)
    telefono_personal = models.IntegerField()
    correo_electronico = models.EmailField()
    TIPO_USUARIO = {
        'arrendatario' : 'arrendatario',
        'arrendador' : 'arrendador'
    }
    tipo_usuario = models.CharField(max_length=12, choices=TIPO_USUARIO)

    def __str__(self) -> str:
        return f'{self.tipo_usuario}: {self.nombre} {self.apellido}'
    
    class Meta:
        ordering = ['rut']
        db_table = 'usuario'
        verbose_name_plural = 'usuarios'


class Inmueble(models.Model):
    propietario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=250)
    m2_construidos = models.FloatField()
    m2_totales = models.FloatField()
    cantidad_estacionamientos = models.IntegerField()
    cantidad_habitaciones = models.IntegerField()
    cantidad_banos = models.IntegerField()
    direccion = models.CharField(max_length=50)
    comuna = models.ForeignKey('Comuna', on_delete=models.DO_NOTHING)
    TIPO_INMUEBLE = {
        'casa' : 'casa',
        'departamento' : 'departamento',
        'parcela' : 'parcela'
    }
    tipo_inmueble = models.CharField(choices=TIPO_INMUEBLE, max_length=20)
    precio_arriendo = models.IntegerField()
    disponible = models.BooleanField()
    solicitudes = models.JSONField()
    arrendatario = models.OneToOneField(Usuario, blank=True, on_delete=models.DO_NOTHING, related_name='arrendatario')

    def __str__(self) -> str:
        return f'{self.tipo_inmueble}: {self.nombre} {self.precio_arriendo} - {self.disponible}'
    
    class Meta:
        ordering = ['tipo_inmueble']
        db_table = 'inmueble'
        verbose_name_plural = 'inmuebles'


class Comuna(models.Model):
    nombre_comuna = models.CharField(max_length=50)
    region = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.region}: {self.nombre_comuna}'
    
    class Meta:
        #ordering = ['region']
        db_table = 'comuna'
        verbose_name_plural = 'comunas'