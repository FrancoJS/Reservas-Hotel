from django.shortcuts import render
from reservas_hotel.models import Cliente, Habitacion, Reserva

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

            opcionesClientes = Cliente.objects.all().order_by("nombre")
            opcionesHabitaciones = Habitacion.objects.all().order_by("tipo")
            datos = {
                'opcionesClientes': opcionesClientes,
                'opcionesHabitaciones': opcionesHabitaciones,
                'r': 'Reserva registrada correctamente!'
            }
            return render(request, 'operador-crear.html', datos)
    else:
        opcionesClientes = Cliente.objects.all().order_by("nombre")
        opcionesHabitaciones = Habitacion.objects.all().order_by("tipo")
        datos = {
            'opcionesClientes': opcionesClientes,
            'opcionesHabitaciones': opcionesHabitaciones,
            'r2': 'Debe seleccionar registrar reserva para continuar'
        }
        return render(request, 'operador-crear.html', datos)
