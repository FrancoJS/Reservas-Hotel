
from django.contrib import admin
from django.urls import path
from reservas_hotel import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mostrar_login),
    path('login', views.iniciar_sesion),
    path('logout', views.cerrar_sesion),
    path('mostrar_historial', views.mostrar_historial),
]
