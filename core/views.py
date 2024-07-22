from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Usuario
from .utilities import cleaned_data
from django.contrib.auth.models import User

# Create your views here.

# a. lograr registrarse en la app
def crear_user(request):
    if request.method == 'POST':
        # método para crear un usuario de django
        user = User.objects.create(
            username = request.POST['username'],
            password = request.POST['password']
            #data = cleaned_data(request.POST)
            #User.objects.create(**data)
        )
        Usuario.objects.create(
            user = user,
            rut = request.POST['rut']
        )
        return redirect('perfil')
    else:
        return render(request, 'registro_usuario.html')


# b. actualizar sus datos
# c. poder identificarse como arrendatario o como arrendador
def actualizar_user(request):
    user = request.user
    usuario = Usuario.objects.filter(user = user)
    if request.method == 'POST':
        data = cleaned_data(request.POST) | {'user':user}
        usuario.update(**data)
        return redirect('perfil')
    else:
        return render(request, 'perfil.html', {'usuario' : usuario})
