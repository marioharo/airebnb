from django.shortcuts import render, redirect
from django.http import HttpResponse
#from django.forms import forms
from .models import Usuario, Comuna, Inmueble
from .utilities import cleaned_data
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return redirect('listar_inmuebles')


# a. lograr registrarse en la app
def crear_usuario(request):
    """ Crea usuarios de 2 tipos que no pertenecen al staff de administradores """
    if request.method == 'GET':
        # data de usuario
        user = request.user
        #usuario = usuario = Usuario.objects.get(user = user)
        context = {'user':user}
        return render(request, 'crear_usuario.html', context)
    else:
        # método para crear un usuario de django
        if request.POST['password'] != request.POST['password_repeat']:
            # raise forms.ValidationError('contraseñas no coinciden')
            return HttpResponse('contraseñas no coinciden, <a href="/crear_usuario">volver</a>')
        else:
            user = User.objects.create_user(
                username = request.POST['username'],
                password = request.POST['password'],
            )
            # el usuario de django creado es parte del modelo "Usuario" con los campos faltantes vacíos
            Usuario.objects.create(
                user = user,
                rut = request.POST['rut'],
            )
            return redirect('exito')
            

@login_required
def exito(request):
    return render(request, 'exito.html')

# c. poder identificarse como arrendatario o como arrendador
@login_required
def perfil(request):
    """ Muestra el perfil tanto de arrendadores como arrendatarios """
    # data de usuario
    user = request.user
    usuario = usuario = Usuario.objects.get(user = user)
    # data de inmueble cuando el usuario es arrendador
    if usuario.tipo_usuario == 'arrendatario':
        inmuebles = Inmueble.objects.filter(arrendatario = usuario)
    else:
        inmuebles = Inmueble.objects.filter(propietario = usuario)
    context = {
        'usuario' : usuario,
        'inmuebles' : inmuebles,
    }
    return render(request, 'perfil.html', context)


# b. actualizar sus datos
@login_required
def actualizar_usuario(request):
    """ Actualiza los campos de un usuario dados en el formulario """
    # data de usuario
    user = request.user
    usuario = Usuario.objects.filter(user = user)
    if request.method == 'GET':
        # data de un único usuario para mostrar el nombre en el título
        usuario_get = Usuario.objects.get(user = user)
        context = {
            'usuario' : usuario,
            'usuario_get' : usuario_get,
            }
        return render(request, 'actualizar_usuario.html', context)
    else:
        # método para modificar un usuario
        # if request.POST['password'] == request.POST['raw_password']:
        #     User.set_password('password', 'raw_password')
        # else:
        #     return HttpResponse('contraseñas no coinciden')
        data = cleaned_data(request.POST) | {'user':user}
        usuario.update(**data)
        return redirect('perfil')


# 3. Un usuario tipo arrendador debe poder:
# a. Publicar sus propiedades en una comuna determinada con sus características.
@login_required
def crear_inmueble(request):
    """ Crea inmueble de 3 tipos difentes a elegir """
    user = request.user
    if request.method == 'POST':
        # instancia de usuario
        usuario = Usuario.objects.get(user = user)
        comuna = Comuna.objects.get(id=request.POST['comuna'])
        data = cleaned_data(request.POST) | {'propietario':usuario, 'comuna':comuna}
        Inmueble.objects.create(**data)
        return redirect('perfil')
    else:
        # data de comunas
        comunas = Comuna.objects.all()
        # data de usuario
        usuario = usuario = Usuario.objects.get(user = user)
        context = {
            'usuario':usuario,
            'comunas':comunas,
            }
        return render(request, 'crear_inmueble.html', context)
    

@login_required
def editar_inmueble(request, id):
    """Edita el inmueble según su id """
    # data de usuario
    user = request.user
    usuario = Usuario.objects.filter(user = user)
    if request.method == 'GET':
        comunas = Comuna.objects.all()
        inmueble = Inmueble.objects.filter(id = id)
        # data de un único inmueble para mostrar el nombre en el título
        inmueble_get = Inmueble.objects.get(id = id)
        context = {
            'inmueble':inmueble,
            'inmueble_get':inmueble_get,
            'comunas':comunas,
            }
        return render(request, 'editar_inmueble.html', context)
    else:
        pk = request.POST['id']
        inmueble = Inmueble.objects.filter(id = pk)
        data = cleaned_data(request.POST)
        inmueble.update(**data)
    return redirect('perfil')


# b. Listar propiedades en el dashboard
def listar_inmuebles(request):
    """Página principal donde se muestra la lista completa de inmuebles """
    user = request.user
    inmuebles = Inmueble.objects.all()
    if request.method == 'GET':
        return render(request, 'listar_inmuebles.html', {'inmuebles':inmuebles})
    else:
        if request.user.is_authenticated:
            # solicitudes de inmueble
            usuario = Usuario.objects.get(user = user)
            inmueble = Inmueble.objects.filter(id = request.POST['id'])
            inmueble.update(solicitudes = {f'{usuario.nombre}' : usuario.rut})
            return redirect('perfil')
        else:
            return redirect('login')


def filtrar_lista_inmuebles(request, id):
    """ Buscador de inmuebles filtrando por Región y comuna """
    return redirect('listar_inmuebles')


@login_required
def solicitud_arriendo(request, id):
    """ Boton de solicitud de arriendo """
    if request.method == 'POST':
        inmueble = Inmueble.objects.filter(id = id)
        inmueble.update(
            solicitudes = {
                f'solicitud_{request.user.username}': request.user.id
            }
        )
    return redirect('perfil')


# c. Eliminar y editar sus propiedades
@login_required
def eliminar_inmueble(request, id):
    Inmueble.objects.get(id = id).delete()
    return redirect('perfil')


def remover_inmueble(request, id):
    pass


# d. Aceptar arrendatarios.
@login_required
def aceptar_arrendatarios(request):
    arrendatario = Usuario.objects.get(id = request.POST['arrendador_id'])
    inmueble = Inmueble.objects.filter(id = request.POST['inmueble_id'])
    inmueble.update(
        solicitud_arriendo = '',
        arrendatario = arrendatario,
        disponible = False,
    )
    return redirect('listar_inmuebles')


def inmueble_comuna(request):
    user = request.user
    usuario = Usuario.objects.filter(user = user)
    if Usuario.tipo_usuario == 'arrendatario':
        if request.method == 'POST':
            comuna = request.POST['comuna']
            comuna = Comuna.objects.get(comuna = comuna)
            inmuebles_comuna = Inmueble.objects.filter(comuna = comuna)
            return render(request, 'inmueble_comuna.html', {'inmuebles_comuna' : inmuebles_comuna})
        else:
            comunas = Comuna.objects.all()
            return render(request, 'listar_propiedades.html', {'comunas' : comunas})
    else:
        return redirect('perfil')