from django.urls import  path,include
from . import views

from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns= [

    path('', views.inicio, name='inicio'),
    path('fiestas', views.fiestas, name='fiestas'),
    path('subir', views.subir, name='subir'),
    path('mapa', views.mapa, name='mapa'),
    path('buscar', views.buscador, name='buscar'),
    path('editar', views.editar, name='editar'),
    path('eliminar/<int:id>', views.eliminar, name='eliminar'),
    path('editar/<int:id>', views.editar, name='editar'),
    path('discotecas', views.discotecas, name='discotecas'),
    path('discoteca/<int:id>', views.discoteca, name='discoteca'),
    path('fiesta/<int:id>', views.fiesta, name='fiesta'),
    path('registrar', views.registrar, name='registrar'),
    path('login', views.login2, name='login'),
    path('logout', views.logout2, name='logout'),
    path('perfil/<str:year>', views.perfil, name='perfil'),
    path('perfil/<str:year>/<str:mes>', views.perfil, name='perfil'),
    path('perfil/<str:year>/<str:mes>/<str:dia>', views.perfil, name='perfil'),
    path('perfil/', views.perfil, name='perfil'),
    path('editar_info/', views.editar_info, name='editar_info'),
    path('cambiar_foto/', views.cambiar_foto, name='cambiar_foto'),
    path('carrito', views.carrito, name='carrito'),
    path('carrito/sumar/<int:id>', views.carritoSuma, name='carritoSuma'),
    path('carrito/restar/<int:id>', views.carritoResta, name='carritoResta'),
    path('carrito/finalizar/<int:id>', views.finalizarCompra, name='finalizarCompra'),
    path('carrito/eliminar/<int:id>', views.carritoElimina, name='eliminarCarrito'),
    path('subscripcion/<int:id>', views.subscripciones, name='subscripcion'),
    path('subscripcion2/<int:id>', views.subscripciones2, name='subscripcion2'),
    path('success/<int:id1>/<int:id2>', views.success, name='success'), #id de la entrada/id carrito
    path('cancel', views.cancel, name='cancel'),
    path('accounts/', include('allauth.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)