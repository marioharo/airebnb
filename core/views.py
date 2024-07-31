from django.shortcuts import render, redirect
from django.http import HttpResponse
#from django.forms import forms
from .models import Usuario, Comuna, Inmueble
from .utilities import cleaned_data
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return redirect('login')


@login_required
def perfil(request):
    # data de usuario
    user = request.user
    usuario = usuario = Usuario.objects.get(user = user)
    # data de inmueble cuando el usuario es arrendador
    if usuario.tipo_usuario == 'arrendador':
        inmuebles = Inmueble.objects.filter(propietario = usuario)
        for inmueble in inmuebles:
            estado = 'Disponible' if inmueble.disponible == True else 'No Disponible'
        context = {
            'usuario': usuario,
            'inmuebles' : inmuebles,
            'estado' : estado,
            }
    else:
        context = {'usuario' : usuario}
    return render(request, 'perfil.html', context)


# a. lograr registrarse en la app
def crear_usuario(request):
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


# b. actualizar sus datos
# c. poder identificarse como arrendatario o como arrendador
@login_required
def actualizar_usuario(request):
    user = request.user
    # data de usuario
    usuario = Usuario.objects.filter(user = user)
    if request.method == 'GET':
        # data de un único usuario
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


def solicitud_arriendo(request, id):
    inmueble = Inmueble.objects.filter(id = id)
    inmueble.update(
        solicitudes = {
            f'solicitud_{request.user.username}': request.user.id
        }
    )
    return redirect('inmueble_comuna')


# 3. Un usuario tipo arrendador debe poder:
# a. Publicar sus propiedades en una comuna determinada con sus características.
@login_required
def crear_inmueble(request):
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
    

# b. Listar propiedades en el dashboard
@login_required
def listar_inmueble(request):
    user = request.user
    inmuebles = Inmueble.objects.filter(propietario = user)
    return render(request, 'listar_inmuebles.html', {'inmuebles' : inmuebles})


# c. Eliminar y editar sus propiedades
@login_required
def eliminar_inmueble(request, id):
    Inmueble.objects.get(id = id).delete()
    return redirect('listar_inmuebles')


@login_required
def editar_inmueble(request, id):
    comuna = Comuna.objects.get(comuna = request.POST['comuna'])
    data = cleaned_data(request.POST) | {'comuna':comuna}
    Inmueble.objects.filter(id = id).update(**data)
    return redirect('listar_inmuebles')


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