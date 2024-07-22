from .models import Usuario, Inmueble, Comuna


# Crear un objeto con el modelo
def crear_inmueble(data):
    propietario = data[0]
    nombre = data[1]
    descripcion = data[2]
    m2_construidos = data[3]
    m2_totales = data[4]
    cantidad_estacionamientos = data[5]
    cantidad_habitaciones = data[6]
    cantidad_banos = data[7]
    direccion = data[8]
    comuna = data[9]
    precio_arriendo = data[10]
    Inmueble.objects.create(
        propietario = propietario,
        nombre = nombre,
        descripcion = descripcion,
        m2_construidos = m2_construidos,
        m2_totales = m2_totales,
        cantidad_estacionamientos = cantidad_estacionamientos,
        cantidad_habitaciones = cantidad_habitaciones,
        cantidad_banos = cantidad_banos,
        direccion = direccion,
        comuna = comuna,
        precio_arriendo = precio_arriendo,
    )

# Enlistar desde el modelo de datos
def obtener_todos_inmuebles():
    inmuebles = Inmueble.objects.all()
    return inmuebles

# Actualizar un registro en el modelo de datos
def actualizar_inmueble(id_inmueble, nueva_descripcion):
    Inmueble.objects.filter(pk = id_inmueble).update(descripcion = nueva_descripcion)

# Borrar un registro del modelo de datos utilizando un modelo Django
def eliminar_inmueble(id_inmueble):
    Inmueble.objects.get(id = id_inmueble).delete()