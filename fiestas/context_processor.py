from .models import Entradas,Carrito,Usuarios
from django.contrib.auth.models import User

def total_carrito(request):
    total=0
    if request.user.is_authenticated:
        username=request.user.username
        lista_nombres=[]
        usuarios=Usuarios.objects.all()
        for u in usuarios:
            lista_nombres.append(u.usuario)
        
        if username not in lista_nombres:
            usuario= Usuarios(usuario=username,foto='/media/imagenes/30995.jpg',correo=request.user.email)
            usuario.save()
            carrito=Carrito(usuarioId=usuario)
            carrito.save()

        else:
            usuario=Usuarios.objects.get(usuario=username)

    if request.user.is_authenticated:
        carrito=Carrito.objects.filter(usuarioId=usuario.usuarioId)
        if carrito.count()>0:
            Id=carrito.first().carritoId
            entradas=Entradas.objects.filter(carritoId=Id)
            for e in entradas:
                total+=e.cantidad
        else:
            total=0
    else:
        if 'carritoId' in request.COOKIES:
            carritoId=request.COOKIES['carritoId']
            carritoId=Carrito.objects.get(carritoId=carritoId).carritoId
            entradas=Entradas.objects.filter(carritoId=carritoId)
            for e in entradas:
                total+=e.cantidad
        else:
            total=0
    
    
    return {"total_carrito": total}
