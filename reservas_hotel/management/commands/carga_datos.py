from django.core.management.base import BaseCommand
from reservas_hotel.models import Usuario, Habitacion, Cliente

class Command(BaseCommand):
    def handle(self, *args, **options):
        lista_clientes = [
            Cliente(nombre='Juan'),
            Cliente(nombre='Maria'),
            Cliente(nombre='Pedro'),
            Cliente(nombre='Luisa'),
            Cliente(nombre='Ana'),
        ]
        Cliente.objects.bulk_create(lista_clientes)
        self.stdout.write('Clientes registrados correctamente!')

        lista_habitaciones = [
            Habitacion(tipo='Individual'),
            Habitacion(tipo='Doble'),
            Habitacion(tipo='Suite'),
            Habitacion(tipo='Familiar'),
            Habitacion(tipo='Presidencial'),
        ]
        Habitacion.objects.bulk_create(lista_habitaciones)
        self.stdout.write('Habitaciones registradas correctamente!')

        lista_usuarios = [
            Usuario(nombre='admin', password='admin123'),
            Usuario(nombre='operador', password='operador123'),
        ]
        Usuario.objects.bulk_create(lista_usuarios)
        self.stdout.write('Usuarios registrados correctamente!')