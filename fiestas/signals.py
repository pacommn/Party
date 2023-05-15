from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Fiestas,Subscripciones
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import requests

#mail1='moisestaba5@gmail.com'
#mail2='robertoac5a@gmail.com'
#mail='pacomorenonavarr@gmail.com'

@receiver(post_save, sender=Fiestas)
def saluda(sender, instance, created, **kwargs):
    if created:
        discoteca=instance.discotecaId.nombre
        fiesta=instance.nombre
        fecha=instance.fecha
        imagen=instance.foto
        ruta="C:/Users/Paco/Desktop/uni/cuarto/TFG/party/party/" + str(imagen)
        print(ruta)

        CLIENT_ID = 'ea115e7d06213e2'

        url = 'https://api.imgur.com/3/image'

        headers = {'Authorization': f'Client-ID {CLIENT_ID}'}

        with open(ruta, 'rb') as f:
            response = requests.post(url, headers=headers, files={'image': f})

        if response.ok:
            # Obtenemos la URL de la imagen subida
            url_imagen = response.json()['data']['link']
            print(f"La imagen ha sido alojada en {url_imagen}")
        else:
            print("Error al subir la imagen")

        urlc="https://aquicompratuentrada.com"

        usuarios_suscritos=Subscripciones.objects.filter(discotecaId=instance.discotecaId)
        lista_usuarios=[]
        for u in usuarios_suscritos:
            lista_usuarios.append(u.usuarioId)
            print(lista_usuarios)

        for usuario in lista_usuarios:

            context={'discoteca':discoteca, 'fiesta':fiesta, 'fecha':fecha, 'usuario':usuario.usuario,'url':urlc,'imagen': url_imagen}
            template=get_template('correo.html')
            content=template.render(context)

            email=EmailMultiAlternatives(
                '¡Únete a nosotros en la fiesta '+ fiesta + ' en ' + discoteca,
                'Paco',
                settings.EMAIL_HOST_USER,
                [usuario.correo]

            )

            email.attach_alternative(content, 'text/html')
            email.send()

