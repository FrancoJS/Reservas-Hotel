from django.shortcuts import render
from reservas_hotel.models import Usuario, Historial
from datetime import datetime


def mostrar_login(request):
    return render(request, 'login.html')


def iniciar_sesion(request):
    if request.method == 'POST':
        nombre_usuario = request.POST['username']
        password = request.POST['password']

        usuario = Usuario.objects.filter(nombre=nombre_usuario, password=password).values()

        if usuario:
            request.session['estado_sesion'] = True
            request.session['nombre_usuario'] = nombre_usuario.upper()
            request.session['id_usuario'] = usuario[0]['id']

            descripcion = "Inicio de Sesion"
            tabla_afectada = ""
            fecha = datetime.now()
            usuario_id = request.session['id_usuario']

            historial = Historial(usuario_id=usuario_id, descripcion=descripcion, tabla_afectada=tabla_afectada, fecha=fecha)
            historial.save()
            datos = {'nombre_usuario': nombre_usuario.upper()}

            if nombre_usuario == 'admin':

                return render(request, 'menu-admin.html', datos)
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
        descripcion = "Cerrar Sesion"
        tabla_afectada = ""
        fecha = datetime.now()
        usuario = request.session['id_usuario']
        historial = Historial(usuario_id=usuario, descripcion=descripcion, tabla_afectada=tabla_afectada, fecha=fecha)
        historial.save()

        del request.session['estado_sesion']
        del request.session['nombre_usuario']
        del request.session['id_usuario']

        return render(request, 'login.html')
    except:
        return render(request, 'login.html')


def mostrar_historial(request):
    try:
        estado_sesion = request.session['estado_sesion']
        nombre_usuario = request.session['nombre_usuario']
        if estado_sesion is True and nombre_usuario == 'ADMIN':
            historial_completo = Historial.objects.select_related('usuario').all().order_by('-fecha')
            datos = {'nombre_usuario': nombre_usuario.upper(), 'historial': historial_completo}
            return render(request, 'admin-historial.html', datos)
        else:
            datos = {'error': '¡No cuenta con los permisos necesarios!'}
            return render(request, 'login.html', datos)
    except:
        datos = {'error': '¡No se puede procesar la solicitud!'}
        return render(request, 'login.html', datos)