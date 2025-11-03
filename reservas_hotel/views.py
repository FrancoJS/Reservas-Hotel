from django.shortcuts import render
from reservas_hotel.models import Usuario


def mostrar_login(request):
    return render(request, 'login.html')


def iniciar_sesion(request):
    if request.method == 'POST':
        nombre_usuario = request.POST['username']
        password = request.POST['password']

        usuario = Usuario.objects.filter(nombre=nombre_usuario, password=password).values()
        print(usuario)

        if usuario:
            request.session['estado_sesion'] = True
            request.session['nombre_usuario'] = nombre_usuario.upper()
            request.session['id_usuario'] = usuario[0]['id']

            datos = {'nombre_usuario': nombre_usuario.upper()}

            if nombre_usuario == 'admin':
                return render(request, 'admin-historial.html', datos)
            else:
                return render(request, '', datos)
        else:
            datos = {'error': '¡El usuario o la contraseña son incorrectos!'}
            return render(request, 'login.html', datos)
    else:
        datos = {'error': '¡No se puede procesar la solicitud!'}
        return render(request, 'login.html')

def cerrar_sesion(request):
    try:
        del request.session['estado_sesion']
        del request.session['nombre_usuario']
        del request.session['id_usuario']

        return render(request, 'login.html')
    except:
        return render(request, 'login.html')
