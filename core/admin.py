from django.contrib import admin
from .models import Comuna, Inmueble, Usuario

# Register your models here.
admin.site.register([Comuna, Inmueble, Usuario])