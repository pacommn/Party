from django.urls import  path
from . import views

from django.conf import settings
from django.contrib.staticfiles.urls import static

app_name="carrito"

urlpatterns= [

    path("agregar/<int:entradaId>",views.agregar_entrada, name="agregar"),
    path("eliminar/<int:entradaId>",views.eliminar_entrada, name="eliminar"),
    path("restar/<int:entradaId>",views.restar_entrada, name="restar"),
    path("limpiar",views.limpiar_carrito, name="limpiar"),

]