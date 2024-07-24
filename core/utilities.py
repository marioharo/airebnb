import csv
from django.contrib.auth.models import User
from .models import Comuna, Inmueble, Usuario

### Cargar datos para poblar db ###
def loaddata_regiones():
    with open('regiones-chile.csv', 'r') as file:
        data = csv.reader(file, delimiter=';')
        data = list(data)
    data.pop(0)
    for d in data:
        Comuna.objects.create(
            nombre_comuna = d[3],
            region = d[0]
        )

# Cargar inmueble
def loaddata_inmueble(propietario_pk:int, comuna_id:int, arrendatario_id:int):
    """Funcion que agrega un nuevo tipo de inmueble a la db desde el archivo <inmueble.csv> ingresando el rut del User"""
    with open('inmueble.csv', 'r') as file:
        data = csv.reader(file, delimiter=',')
        data = list(data)
    data.pop(0)
    # instancia de propietario
    propietario_fk = Usuario.objects.get(rut = propietario_pk)

    for d in data:
        Inmueble.objects.create(
            propietario = propietario_fk,
            nombre = d[2],
            descripcion = d[3],
            m2_construidos = d[4],
            m2_totales = d[5],
            cantidad_estacionamientos = d[6],
            cantidad_habitaciones = d[7],
            cantidad_banos = d[8],
            direccion = d[9],
            comuna = comuna_id,
            tipo_inmueble = d[11],
            precio_arriendo = d[12],
            disponible = d[13],
            #solicitudes = d[jsonfield],
            arrendatario = arrendatario_id,
        )

### Cargar usuario
def loaddata_usuario(rut:int):
    """Funcion que agrega un nuevo tipo de usuario a la db desde el archivo <usuario.csv> ingresando el rut del User"""
    with open('usuario.csv', 'r') as file:
        data = csv.reader(file, delimiter=',')
        data = list(data)
        data.pop(0)

        for d in data:
            Usuario.objects.create(
                user = rut,
                rut = d[1],
                nombre = d[2],
                apellido = d[3],
                direccion = d[4],
                telefono_personal = d[5],
                correo_electronico = d[6],
                tipo_usuario = d[7],
            )

### funciones de utilidad ###
cleaned_data = lambda x:{k:v for k,v in x.items() if k != 'csrfmiddlewaretoken'}

def get_model_headers(model):
    """Rescata uno a uno los encabezados de los models separandolos por comas"""
    return [field.name for field in model._meta.fields]

def guardar_data_csv():
    """Función para crear csv con los encabezamos (headers) del modelo ingresado"""
    headers = get_model_headers(Usuario)
    with open('usuario.csv', 'w') as file:
        data = csv.writer(file)
        data.writerow(headers)

