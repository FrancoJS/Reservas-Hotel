from django.shortcuts import render
from reservas_hotel.models import Usuario, Historial, Reserva, Cliente, Habitacion
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
                return render(request, 'menu-operador.html', datos)
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

def mostrar_operador(request):
    datos = {'nombre_usuario': request.session['nombre_usuario'].upper()}
    return render(request, 'menu-operador.html', datos)

def mostrar_registrar(request):
    opcionesClientes = Cliente.objects.all().order_by("nombre")
    opcionesHabitaciones = Habitacion.objects.all().order_by("tipo")
    datos = {
            'opcionesClientes': opcionesClientes,
            'opcionesHabitaciones': opcionesHabitaciones,

    }
    return render(request, 'operador-crear.html', datos)


def registrarReserva(request):
    if request.method == 'POST':
        cli = request.POST['cbocli']
        hab = request.POST['cbohab']
        fec = request.POST['txtfec']
        mon = request.POST['txtmon']

        comprobarReserva = Reserva.objects.filter(cliente_id=cli, fecha_reserva=fec)
        if comprobarReserva:
            opcionesClientes = Cliente.objects.all().order_by("nombre")
            opcionesHabitaciones = Habitacion.objects.all().order_by("tipo")
            datos = {
                'opcionesClientes': opcionesClientes,
                'opcionesHabitaciones': opcionesHabitaciones,
                'r2': 'El cliente seleccionado ya tiene una reserva para esa fecha!'
            }
            return render(request, 'operador-crear.html', datos)
        else:
            nueva = Reserva(cliente_id=cli, habitacion_id=hab, fecha_reserva=fec, monto=mon)
            nueva.save()

            descripcion = "Registrar Reserva"
            tabla_afectada = "Reserva"
            fecha = datetime.now()
            usuario = request.session['id_usuario']
            historial = Historial(usuario_id=usuario, descripcion=descripcion, tabla_afectada=tabla_afectada, fecha=fecha)
            historial.save()

            opcionesClientes = Cliente.objects.all().order_by("nombre")
            opcionesHabitaciones = Habitacion.objects.all().order_by("tipo")
            datos = {
                'opcionesClientes': opcionesClientes,
                'opcionesHabitaciones': opcionesHabitaciones,
                'r': 'Reserva registrada correctamente!'
            }
            return render(request, 'operador-crear.html', datos)

def listarReserva(request):
    estado_sesion = request.session['estado_sesion']
    if estado_sesion is True:
        if request.session['nombre_usuario'] != 'ADMIN':
            lista = Reserva.objects.select_related("cliente", "habitacion").order_by("id")
            habitaciones = Habitacion.objects.all().order_by("tipo")
            clientes = Cliente.objects.all().order_by("nombre")

            nombre_cliente = request.GET.get('cliente', '')
            Habitacion_id = request.GET.get('habitacion', '')
            fecha_reserva = request.GET.get('fecha', '')

            if nombre_cliente:
                lista = lista.filter(cliente_id=nombre_cliente)
            if Habitacion_id:
                lista = lista.filter(habitacion_id=Habitacion_id)
            if fecha_reserva:
                lista = lista.filter(fecha_reserva__icontains=fecha_reserva)

            datos = {
                'nombre_usuario': request.session['nombre_usuario'].upper(),
                'lista': lista,
                'habitaciones': habitaciones,
                'clientes': clientes
            }
            return render(request, 'operador-listado.html', datos)
        else:
            datos = {
                'r2': '¡No cuenta con los permisos necesarios!'
            }
            return render(request, 'login.html', datos)
    else:
        datos = {
            'r2': '¡No se puede procesar la solicitud!'

        }
        return render(request, 'login.html', datos)
    

def mostrar_editar(request, id):
    try:
        estado_sesion = request.session['estado_sesion']
        if estado_sesion is True:
            reserva = Reserva.objects.get(id=id)
            opcionesClientes = Cliente.objects.all().order_by("nombre")
            opcionesHabitaciones = Habitacion.objects.all().order_by("tipo")

            if request.method == 'POST':
                cli = request.POST['cbocli']
                hab = request.POST['cbohab']
                fec = request.POST['txtfec']
                mon = request.POST['txtmon']

                comprobarReserva = Reserva.objects.filter(cliente_id=cli, fecha_reserva=fec).exclude(id=id)
                if comprobarReserva:
                    datos = {
                        'reserva': reserva,
                        'opcionesClientes': opcionesClientes,
                        'opcionesHabitaciones': opcionesHabitaciones,
                        'r2': 'El cliente seleccionado ya tiene una reserva para esa fecha!'
                    }
                    return render(request, 'operador-editar.html', datos)
                else:
                    reserva.cliente_id = cli
                    reserva.habitacion_id = hab
                    reserva.fecha_reserva = fec
                    reserva.monto = mon
                    reserva.save()

                    descripcion = "Editar Reserva"
                    tabla_afectada = "Reserva"
                    fecha = datetime.now()
                    usuario = request.session['id_usuario']
                    historial = Historial(usuario_id=usuario, descripcion=descripcion, tabla_afectada=tabla_afectada, fecha=fecha)
                    historial.save()

                    datos = {
                        'reserva': reserva,
                        'opcionesClientes': opcionesClientes,
                        'opcionesHabitaciones': opcionesHabitaciones,
                        'r': 'Reserva actualizada correctamente!'
                    }
                    return render(request, 'operador-editar.html', datos)
            else:
                datos = {
                    'reserva': reserva,
                    'opcionesClientes': opcionesClientes,
                    'opcionesHabitaciones': opcionesHabitaciones
                }
                return render(request, 'operador-editar.html', datos)
        else:
            datos = {'r2': '¡No se puede procesar la solicitud!'}
            return render(request, 'login.html', datos)

    except Reserva.DoesNotExist:
        datos = {'r2': f"El ID ({id}) No existe. Imposible editar!!"}
        return render(request, 'operador-editar.html', datos)

def eliminarReserva(request, id):
    try:
        res = Reserva.objects.get(id=id)
        cliente = res.cliente.nombre
        habitacion = res.habitacion.tipo
        fecha = res.fecha_reserva
        referencia = f"{cliente} - {habitacion}"

        res.delete()

        descripcion = "Eliminar Reserva"
        tabla_afectada = "Reserva"
        fecha = datetime.now()
        usuario = request.session['id_usuario']
        historial = Historial(usuario_id=usuario, descripcion=descripcion, tabla_afectada=tabla_afectada, fecha=fecha)
        historial.save()

        reservas = Reserva.objects.select_related("cliente", "habitacion").order_by("fecha_reserva")
        datos = {
            'reservas': reservas,
            'r': f"Reserva: {referencia} eliminada correctamente!"
        }
        return render(request, 'operador-eliminar.html', datos)

    except Reserva.DoesNotExist:
        reservas = Reserva.objects.select_related("cliente", "habitacion").order_by("fecha_reserva")
        datos = {
            'reservas': reservas,
            'r2': f"El ID ({id}) No Existe. Imposible Eliminar!!"
        }
        return render(request, 'operador-eliminar.html', datos)
