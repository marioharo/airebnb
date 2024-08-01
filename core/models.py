from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserModel

# Create your models here.
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)
    telefono_personal = models.IntegerField(null=True)
    correo_electronico = models.EmailField()
    TIPO_USUARIO = {
        'arrendatario' : 'arrendatario',    
        'arrendador' : 'arrendador'
    }
    tipo_usuario = models.CharField(max_length=12, choices=TIPO_USUARIO)

    def __str__(self) -> str:
        return f'{self.rut} {self.nombre} {self.apellido}: {self.tipo_usuario}'
    
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
    solicitudes = models.JSONField(null=True, blank=True)
    arrendatario = models.OneToOneField(Usuario, null=True, on_delete=models.DO_NOTHING, related_name='arrendatario')

    def __str__(self) -> str:
        estado = 'Disponible' if self.disponible == True else 'No Disponible'
        return f'{self.id} {self.tipo_inmueble} ({estado}) ubicado en: {self.comuna.nombre_comuna} | (Dueño: {self.propietario.nombre})'
    
    class Meta:
        ordering = ['id']
        db_table = 'inmueble'
        verbose_name_plural = 'inmuebles'


class Comuna(models.Model):
    nombre_comuna = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    

    def __str__(self) -> str:
        return f'{self.id} {self.region}: {self.nombre_comuna}'
    
    class Meta:
        #ordering = ['id']
        db_table = 'comuna'
        verbose_name_plural = 'comunas'