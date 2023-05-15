from django.shortcuts import render

from .carrito import Carrito
from fiestas.models import Entradas
from django.shortcuts import redirect

# Create your views here.

def agregar_entrada(request,id):
    carrito=Carrito(request)
    entrada=Entradas.objects.get(entradaId=id)
    carrito.agregar(entradas=entrada)
    return redirect("fiestas")


def eliminar_entrada(request,id):
    carrito=Carrito(request)
    entrada=Entradas.objects.get(entradaId=id)
    carrito.eliminar(entradas=entrada)
    return redirect("fiestas")

def restar_entrada(request,id):
    carrito=Carrito(request)
    entrada=Entradas.objects.get(entradaId=id)
    carrito.restar_entradas(entradas=entrada)
    return redirect("fiestas")


def limpiar_carrito(request,id):
    carrito=Carrito(request)
    carrito.limpiar_carrito()
    return redirect("fiestas")

