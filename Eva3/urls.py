from django.contrib import admin
from django.urls import path
from reservas_hotel import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('operador-crear/', views.registrarReserva)
]
