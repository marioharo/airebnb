from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario, Comuna, Inmueble
from .utilities import cleaned_data
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return redirect('crear_usuario')


# a. lograr registrarse en la app
def crear_usuario(request):
    if request.method == 'GET':
        return render(request, 'crear_usuario.html')
    else:
        # método para crear un usuario de django
        if request.POST['password'] == request.POST['password_repeat']:
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
        else:
            return HttpResponse('Contraseñas no coinciden, intentelo de nuevo')


def exito(request):
    return render(request, 'exito.html')


# b. actualizar sus datos
# c. poder identificarse como arrendatario o como arrendador
@login_required
def actualizar_user(request):
    user = request.user
    usuario = Usuario.objects.get(user = user)
    if request.method == 'POST':
        data = cleaned_data(request.POST) | {'user':user}
        usuario.update(**data)
        return redirect('perfil')
    else:
        return render(request, 'perfil.html', {'usuario' : usuario})


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
    if request.method == 'POST':
        user = request.user
        comuna = Comuna.objects.get(comuna = request.POST['comuna'])
        data = cleaned_data(request.POST) | {'propietario':user, 'comuna':comuna}
        Inmueble.objects.create(**data)
        return redirect('crear_inmueble')
    else:
        return render(request, 'crear_inmueble')
    

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