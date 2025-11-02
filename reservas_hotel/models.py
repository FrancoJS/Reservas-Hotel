from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=15)
    password = models.CharField(max_length=20)

class Habitacion(models.Model):
    tipo = models.CharField(max_length=100)

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)

class Reserva(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField()
    monto = models.IntegerField()

class Historial(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    tabla_afectada = models.CharField(max_length=100)
    fecha = models.DateTimeField()