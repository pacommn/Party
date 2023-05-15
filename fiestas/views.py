from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Discotecass,Usuarios,Entradas,Fiestas,Fotos,Carrito,Subscripciones
from .forms import DiscotecasForm, UserForm,LoginForm, FotosForm,EntradaForm,UserForm2
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime,date
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template.loader import get_template
import pdfkit
from django.http import FileResponse
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import os
import requests
from easy_pdf.views import PDFTemplateResponseMixin
from django.views.generic import DetailView
from easy_pdf.rendering import render_to_pdf_response
from io import BytesIO
from xhtml2pdf import pisa
from django.contrib import messages
import qrcode
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


# Create your views here.


def buscador(request):
    nombre= request.GET.get('nombre')

    if nombre:
        resultado=Discotecass.objects.filter(nombre__icontains=nombre)
        if resultado.count() > 0:
            disco=resultado.first()
            id=disco.discotecaId
            print(disco.nombre)
            return discoteca(request,id)
        else:
            request.session['mensaje']=nombre
            return redirect('/discotecas')

def discotecas(request):
    x=False
    mensaje=request.session.get('mensaje')
    print(mensaje)
    if mensaje!=None:
        x=True
        messages.warning(request, mensaje)
        request.session['mensaje']=None

    if request.user.is_authenticated:
        username=request.user.username
        usuario=Usuarios.objects.get(usuario=username)
        lista_pintadas=[]
        discos=Subscripciones.objects.filter(usuarioId=usuario.usuarioId)
        for d in discos:
            lista_pintadas.append(d.discotecaId.nombre)
    else:
        usuario="peppepe"
        lista_pintadas=[]
    discotecas=Discotecass.objects.all()
    
    return render(request, 'discotecas.html',{'usuario': usuario,'discotecas': discotecas,'lista_pintadas':lista_pintadas,'mensaje':mensaje,'x':x})
    

def inicio(request):
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
            
    else:
        usuario="peppepe"
    return render(request, 'inicio2.html', {'usuario': usuario})

def mapa(request):
    if request.user.is_authenticated:
        username=request.user.username
        usuario=Usuarios.objects.get(usuario=username)
    else:
        usuario="peppepe"
    return render(request, 'mapa.html', {'usuario': usuario})

def finalizarCompra(request,id):
    entradas=Entradas.objects.filter(carritoId=id)
    for e in entradas:
        e.pagado=1
        e.carritoId=None
        e.save()
        cantidad=e.cantidad
        dni=e.dni
        nombre=e.nombre
        fecha=e.fiestaId.fecha
        precio=e.coste

        imagen=e.fiestaId.foto
        ruta="C:/Users/Paco/Desktop/uni/cuarto/TFG/party/party/" + str(imagen)
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

        ruta="file:///C:/Users/Paco/Desktop/uni/cuarto/TFG/party/party/" + str(imagen)
        fiesta=e.fiestaId.nombre
        discoteca=e.fiestaId.discotecaId.nombre
        tipo=e.tipo
        if tipo=='N':
            tipo='Normal'
        else:
            tipo='Reservado'

        for i in range(cantidad):
            data_qr = str(nombre) + '_' + str(fiesta) + '_' + str(e.entradaId) + '_' + str(i)
            data_qr_utf8 = data_qr.encode('utf-8')
            qr=qrcode.QRCode(version=1,box_size=10,border=5)
            qr.add_data(data_qr_utf8)
            qr.make(fit=True)
            img=qr.make_image(fill='black',back_color='white')
            nombre_qr=data_qr +'.png'
            qr_path = os.path.join(settings.MEDIA_ROOT, 'entradas_qr', nombre_qr)
            img.save(qr_path)
            ruta_qr="file:///C:/Users/Paco/Desktop/uni/cuarto/TFG/party/party/entradas_qr/" + nombre_qr

            context={'discoteca':discoteca, 'tipo':tipo, 'fecha':fecha,'imagen':ruta, 'usuario':nombre,'dni':dni,'precio':precio,
                     'imagen_qr':ruta_qr,'data_qr':data_qr}
            
            template=get_template('entrada_pdf.html')
            content=template.render(context)
            print("1")
            #template = 'entrada_pdf.html'
            #pdf = render_to_pdf(template, context)
            #return HttpResponse(pdf, content_type='application/pdf')
            config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
            pdf_filename = str(nombre) + '_' + str(fiesta) +  '_' + str(e.entradaId) + '_' + str(i) + '.pdf'
            pdf_path = os.path.join(settings.MEDIA_ROOT, 'entradas_pdf', pdf_filename)
            pdf_bytes = pdfkit.from_string(content, configuration=config, options={"enable-local-file-access": None})
            print("2")
            with open(pdf_path, 'wb') as pdf_file:
                pdf_file.write(pdf_bytes)

            print("3")
            context={'discoteca':discoteca, 'fiesta':fiesta, 'fecha':fecha, 'usuario':e.nombre,'imagen':url_imagen}
            template=get_template('correo_entrega.html')
            content=template.render(context)
            print("4")
            email=EmailMultiAlternatives(
                '¡Gracias por tu compra!',
                'Paco',
                settings.EMAIL_HOST_USER,
                [e.correo_de_entrega]

            )

            email.attach_alternative(content, 'text/html')
            email.attach(pdf_filename, pdf_bytes, 'application/pdf')
            email.send()

    return redirect('carrito')

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def carritoElimina(request,id):
    entrada=Entradas.objects.get(entradaId=id)
    entrada.delete()
    return redirect('carrito')


def carritoSuma(request,id):
    entrada=Entradas.objects.get(entradaId=id)
    entrada.cantidad+=1
    entrada.save()
    return redirect('carrito')

def carritoResta(request,id):
    entrada=Entradas.objects.get(entradaId=id)
    if entrada.cantidad-1 == 0:
        entrada.delete()
    else:
        entrada.cantidad-=1
        entrada.save()
    return redirect('carrito')

def carrito(request):
    if request.user.is_authenticated:
        username=request.user.username
        usuario=Usuarios.objects.get(usuario=username)
    else:
        usuario="peppepe"
    if request.user.is_authenticated:
        carritoId=Carrito.objects.get(usuarioId=usuario.usuarioId).carritoId
    else:
        print ("Aqui")
        carritoId=request.COOKIES['carritoId']
        carritoId=Carrito.objects.get(carritoId=carritoId).carritoId
    total=0
    entradas=Entradas.objects.filter(carritoId=carritoId)
    for e in entradas:
        total+=e.total
    n=len(entradas)
    return render(request, 'carrito.html', {'usuario': usuario,'entradas': entradas,'n': n, 'total': total,'carritoId': carritoId})


def subscripciones(request,id):
    username=request.user.username
    usuario=Usuarios.objects.get(usuario=username)
    existe=Subscripciones.objects.filter(usuarioId=usuario.usuarioId,discotecaId=id)
    if existe.count()>0:
        existe.first().delete()
    else:
        discoteca=Discotecass.objects.get(discotecaId=id)
        s=Subscripciones(usuarioId=usuario,discotecaId=discoteca)
        s.save()

    return redirect('discotecas')



def subscripciones2(request,id):
    username=request.user.username
    usuario=Usuarios.objects.get(usuario=username)
    d=1
    existe=Subscripciones.objects.filter(usuarioId=usuario.usuarioId,discotecaId=id)
    if existe.count()>0:
        existe.first().delete()
    else:
        discoteca=Discotecass.objects.get(discotecaId=id)
        s=Subscripciones(usuarioId=usuario,discotecaId=discoteca)
        s.save()
    url = reverse('perfil') 
    query_string = f'?d={d}'
    return redirect(f'{url}{query_string}')

def fiestas(request):
    if request.user.is_authenticated:
        username=request.user.username
        usuario=Usuarios.objects.get(usuario=username)
    else:
        usuario="peppepe"
    fiestas=Fiestas.objects.filter(fecha__gte=date.today()).order_by('fecha')
    return render(request, 'fiestas.html',{'usuario': usuario, 'fiestas': fiestas})

def fiesta(request,id):
    formulario=EntradaForm(request.POST or None)
    fiesta=Fiestas.objects.get(fiestaId=id)
    if request.user.is_authenticated:
        username=request.user.username
        usuario=Usuarios.objects.get(usuario=username)
        carrito = Carrito.objects.get(usuarioId=usuario.usuarioId)
    else:
        if 'carritoId' in request.COOKIES:
            print('Aqui1')
            # si hay un identificador de carrito almacenado en la cookie, busca el carrito en la sesión
            carrito_id = request.COOKIES['carritoId']
            carrito = request.session.get('carrito', None)
            carrito=Carrito.objects.get(carritoId=carrito_id)
            if carrito is None:
                print('Aqui2')
                # si el carrito no está en la sesión, crea uno nuevo
                carrito = Carrito.objects.create()
                # almacena el identificador único del carrito en la sesión
                request.session['carrito'] = carrito.to_dict()
        else:
           
            # si no hay un identificador de carrito almacenado en la cookie, crea uno nuevo
            carrito = Carrito.objects.create()
            # almacena el identificador único del carrito en la cookie
            response = HttpResponse()
            response = redirect('/fiesta/'+str(id))
            response.set_cookie('carritoId', carrito.carritoId)
            # almacena el identificador único del carrito en la sesión
            request.session['carrito'] = carrito.to_dict()
            return response
            
        usuario="peppepe"

    if formulario.is_valid():
        nombre=formulario.cleaned_data['nombre']
        dni=formulario.cleaned_data['dni']
        cantidad=formulario.cleaned_data['cantidad']
        tipo=formulario.cleaned_data['tipo']
        if request.user.is_authenticated and usuario.correo:
            correo=usuario.correo
            print("aqui")
            entrada_repetida=Entradas.objects.filter(fiestaId=fiesta.fiestaId, carritoId=carrito.carritoId, tipo=tipo,dni=dni,nombre=nombre)
            if entrada_repetida.count() > 0:
                entrada=entrada_repetida.first()
                entrada.cantidad +=cantidad
            else:
                entrada=Entradas(tipo=tipo,coste=fiesta.precio, dni=dni,nombre=nombre,cantidad=cantidad,discotecaId=fiesta.discotecaId,fiestaId=fiesta,usuarioId=usuario,pagado=0,carritoId=carrito,correo_de_entrega=correo)
        
        elif request.user.is_authenticated:
            correo=formulario.cleaned_data['correo_de_entrega']
            print("aqui")
            entrada_repetida=Entradas.objects.filter(fiestaId=fiesta.fiestaId, carritoId=carrito.carritoId, tipo=tipo,dni=dni,nombre=nombre)
            if entrada_repetida.count() > 0:
                entrada=entrada_repetida.first()
                entrada.cantidad +=cantidad
            else:
                entrada=Entradas(tipo=tipo,coste=fiesta.precio, dni=dni,nombre=nombre,cantidad=cantidad,discotecaId=fiesta.discotecaId,fiestaId=fiesta,usuarioId=usuario,pagado=0,carritoId=carrito,correo_de_entrega=correo)
        
        else:
            correo=formulario.cleaned_data['correo_de_entrega']
            entrada_repetida=Entradas.objects.filter(fiestaId=fiesta.fiestaId, carritoId=carrito.carritoId, tipo=tipo,dni=dni,nombre=nombre)
            if entrada_repetida.count() > 0:
                entrada=entrada_repetida.first()
                entrada.cantidad +=cantidad
            else:
                entrada=Entradas(tipo=tipo,coste=fiesta.precio, dni=dni,nombre=nombre,cantidad=cantidad,discotecaId=fiesta.discotecaId,fiestaId=fiesta,pagado=0,carritoId=carrito,correo_de_entrega=correo)

        entrada.save()
        
    
    return render(request, 'fiesta.html',{'usuario': usuario,'fiesta': fiesta,'formulario': formulario, 'id': id})

def discoteca(request,id):
    if request.user.is_authenticated:
        username=request.user.username
        usuario=Usuarios.objects.get(usuario=username)
    else:
        usuario="peppepe"
    discoteca=Discotecass.objects.get(discotecaId=id)
    fiestas=Fiestas.objects.filter(discotecaId=id,fecha__gte=date.today())
    fotos=Fotos.objects.filter(discotecaId=id)
    return render(request, 'discoteca.html',{'usuario': usuario,'discoteca': discoteca,'fiestas': fiestas, 'fotos':fotos})



def subir(request):
    formulario=FotosForm(request.POST or None , request.FILES or None)
    username=request.user.username
    usuario=Usuarios.objects.get(usuario=username)
    discotecaId=usuario.discotecaId
    if formulario.is_valid():
        for imagen in request.FILES.getlist('foto'):
            foton=Fotos(foto=imagen,discotecaId=discotecaId)
            foton.save()
        return redirect('subir')
    fotos=Fotos.objects.filter(discotecaId=discotecaId)
    paginator = Paginator(fotos, 4)
    page = request.GET.get('page')
    try:
        fotos = paginator.page(page)
    except PageNotAnInteger:
        fotos = paginator.page(1)
    except EmptyPage:
        fotos = paginator.page(paginator.num_pages)
    return render(request,'subir.html',{'fotos':fotos, 'formulario':formulario , 'usuario': usuario})

def editar(request, id):
    discoteca=Discotecass.objects.get(discotecaId=id)
    usuario=request.user.username
    formulario=DiscotecasForm(request.POST or None, request.FILES or None , instance=discoteca)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('subir')
    return render(request, 'editar.html',{'formulario':formulario , 'usuario': usuario})

def eliminar(request, id):
    discoteca=Discotecass.objects.get(discotecaId=id)
    discoteca.delete()
    return redirect('subir')

def registrar(request):
    formulario=UserForm(request.POST or None,request.FILES or None)
    usuario=request.user.username
    if formulario.is_valid():
        formulario.save()
        user=User.objects.create_user(username=request.POST['usuario'],password=request.POST['contraseña'],email=request.POST['correo'])
        user.save()
        print(user.username)
        usuarioId=Usuarios.objects.get(usuario=user.username)
        carrito=Carrito(usuarioId=usuarioId)
        carrito.save()
        login(request,user)
        return redirect('discotecas')
    return render(request,'registrar.html',{'formulario':formulario, 'request':request, 'usuario': usuario})

def editar_info(request):
    if request.user.is_authenticated:
        username=request.user.username
        usuario=Usuarios.objects.get(usuario=username)
    else:
        usuario="peppepe"
    id=Usuarios.objects.get(usuario=username).usuarioId
    user=Usuarios.objects.get(usuarioId=id)
    formulario=UserForm2(request.POST or None ,instance=user)
    
    if formulario.is_valid():
        formulario.save()
        user2=User.objects.get(id=id)
        user2.email=formulario.cleaned_data["correo"]
        user2.username=formulario.cleaned_data["usuario"]
        user2.save()
        return redirect('perfil')
    return render(request,'editar_info.html',{'formulario':formulario, 'request':request, 'usuario': usuario})

def cambiar_foto(request):
    print('aqui')
    if request.method == 'POST':
        archivo = request.FILES['file2']
        usuario=request.user.username
        user=Usuarios.objects.get(usuario=usuario)
        user.foto= '/imagenes/imagenes/'+ archivo.name
        user.save()

        fs = FileSystemStorage()
        filename = fs.save('imagenes/' + archivo.name, archivo)
        # Guarda el archivo en algún lugar de almacenamiento permanente en el servidor
        # O guárdalo en el modelo de usuario
        return redirect('perfil') # Redirige a la página de perfil después de cargar la imagen
    else:
        return HttpResponse('Método no válido')

    
def login2(request):
    if request.method == 'POST':
        formulario = LoginForm(request.POST or None)
        if formulario.is_valid():
            username = formulario.cleaned_data['username']
            password = formulario.cleaned_data['contrasena']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('discotecas')
            else:
                if Usuarios.objects.filter(usuario=username).exists():
                    formulario.add_error("contrasena", "La contraseña es incorrecta")
                else:
                    formulario.add_error("username", "El usuario no existe")
        else:
            print ("aqui")
    else:
        formulario=LoginForm()  
    
    return render(request, 'login.html', {'formulario': formulario,'request': request})

@login_required
def logout2(request):
    logout(request)
    return redirect('login')


def perfil(request,dia='01',year='2023',mes='Enero'):
    #print(year)
    meses=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    diccionario_meses={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
    username=request.user.username
    usuario=Usuarios.objects.get(usuario=username)
    
    entrad=Entradas.objects.filter(usuarioId=usuario.usuarioId,fiestaId__fecha__gte=date.today()).order_by('fiestaId__fecha')
    entradas=[]
    for e in entrad:
        entradas.append((e,range(e.cantidad)))

    discos=Subscripciones.objects.filter(usuarioId=usuario.usuarioId)
    discotecas=[]
    for d in discos:
        discotecas.append(d.discotecaId)
    n=len(discotecas)
    lista_valores_entradas,lista_valores_facturados=calculo_grafico1_grafico2(request,year)
    lista_fechas=lista_fechas_entradas(request,year,diccionario_meses[mes])
    lista_dias_fiestas,dicc=dias_fiestas(dia,diccionario_meses[mes],year,usuario)
    numero_dias=len(lista_dias_fiestas)
    lista_fechas_2=list(map(str,lista_dias_fiestas))
    #print(numero_dias)
    if numero_dias==0:
        texto='No hay ningun registro de entradas'
        no_vendidas=0
        normal=0
        reservado=0
    else:
        url=request.build_absolute_uri().split('/')
        if len(url)<7:
            #print (lista_fechas)
            dia=lista_dias_fiestas[0]
        no_vendidas,normal,reservado=calculo_grafico4(dia,diccionario_meses[mes],year,usuario)
        texto='Entradas del dia '+ str(dia) + ' de ' + mes + ' del ' + year
    cantidad_entradas,cantidad_facturado=calculo_grafico5(diccionario_meses[mes],year,lista_dias_fiestas,dicc,usuario)
    sumatorio1=sum(cantidad_facturado)
    sumatorio2=sum(cantidad_entradas)
    valores1,valores2=calculo_grafico3(request,year,diccionario_meses[mes],lista_fechas)
    sum1=sum(valores1)
    sum2=sum(valores2)
    #print (mes)
    sumatorio_entradas=sum(lista_valores_entradas)
    sumatorio_facturados=sum(lista_valores_facturados)
    return render(request, 'perfil.html',{'usuario': usuario , 'lista_valores_entradas': lista_valores_entradas , 'year':year , 
            'sumatorio_entradas': sumatorio_entradas , 'lista_valores_facturados': lista_valores_facturados , 
            'sumatorio_facturados': sumatorio_facturados , 'meses':meses , 'mes':mes ,'lista_fechas':lista_fechas , 'valores1' :valores1 ,
            'valores2' :valores2 , 'dia' :dia ,'numero_dias':numero_dias,'texto':texto,'lista_fechas_2': lista_fechas_2,
            'cantidad_facturado':cantidad_facturado, 'cantidad_entradas':cantidad_entradas, 'lista_dias_fiestas':lista_dias_fiestas,
            'sumatorio1':sumatorio1, 'sumatorio2':sumatorio2, 'sum1':sum1,'sum2':sum2,'no_vendidas':no_vendidas,'normal':normal,
            'reservado':reservado,'n':n,'discotecas':discotecas, 'entradas':entradas })


def calculo_grafico1_grafico2(request,year):
    username=request.user.username
    usuario=Usuarios.objects.get(usuario=username)
    lista_valores_entradas=[]
    lista_valores_facturados=[]
    for m in range(1,13):
        suma_entradas=0
        suma_facturado=0
        objetos=Entradas.objects.filter(fiestaId__fecha__year=year, fiestaId__fecha__month=m,discotecaId=usuario.discotecaId,pagado=1)
        for m in objetos:
            suma_entradas+=m.cantidad
            suma_facturado+=m.coste*m.cantidad
        lista_valores_entradas.append(float(suma_entradas))
        lista_valores_facturados.append(float(suma_facturado))
    return lista_valores_entradas, lista_valores_facturados

def lista_fechas_entradas(request,year,mes):
    username=request.user.username
    usuario=Usuarios.objects.get(usuario=username)
    lista_fechas=[]
    entradas=Entradas.objects.filter(fecha__year=year,fecha__month=mes,discotecaId=usuario.discotecaId,pagado=1)
    for e in entradas:
        lista_fechas.append(e.fecha.day)
    lista_fechas=set(lista_fechas)
    lista_fechas=list(lista_fechas)
    return lista_fechas

def calculo_grafico3(request,year,mes,lista_fechas):
    username=request.user.username
    usuario=Usuarios.objects.get(usuario=username)
    valores1=[]
    valores2=[]
    for d in lista_fechas:
        entradas=Entradas.objects.filter(fecha__year=year,fecha__month=mes,discotecaId=usuario.discotecaId,fecha__day=d,pagado=1)
        suma1=0
        suma2=0
        for e in entradas:
            suma1+=e.cantidad
            suma2+=e.cantidad*e.coste
        valores1.append(float(suma1))
        valores2.append(float(suma2))
    
    return valores1,valores2

def calculo_grafico5(mes,year,lista_dias_fiestas,dicc,usuario):
    cantidad_entradas = []
    cantidad_facturado=[]
    for d in lista_dias_fiestas:
        lista1=[]
        lista2=[]
        mes=int(mes)
        year=int(year)
        dat = date(year, mes, d )
        entradas=Entradas.objects.filter(fiestaId=dicc[dat],discotecaId=usuario.discotecaId,pagado=1)
        for e in entradas:
            lista1.append(e.cantidad)
            lista2.append(e.cantidad*e.coste)
        cantidad_entradas.append(sum(lista1))
        cantidad_facturado.append(float(sum(lista2)))
    return cantidad_entradas,cantidad_facturado 

def dias_fiestas(dia,mes,year,usuario):
    lista=[]
    dicc={}
    fiestas=Fiestas.objects.filter(fecha__year=year,fecha__month=mes,discotecaId=usuario.discotecaId)
    for f in fiestas:
        dicc[f.fecha]=f
        lista.append(f.fecha.day)
    lista.sort()
    return lista,dicc

def calculo_grafico4(dia,mes,year,usuario):
    normal=0
    reservado=0
    normales=Entradas.objects.filter(fiestaId__fecha__day=dia,fiestaId__fecha__month=mes,fiestaId__fecha__year=year,discotecaId=usuario.discotecaId,tipo='N',pagado=1)
    for n in normales:
        normal+=n.cantidad
    reservados=Entradas.objects.filter(fiestaId__fecha__day=dia,fiestaId__fecha__month=mes,fiestaId__fecha__year=year,discotecaId=usuario.discotecaId, tipo='R',pagado=1)
    for r in reservados:
        reservado+=r.cantidad
    total_entradas=Fiestas.objects.filter(fecha__year=year,discotecaId=usuario.discotecaId,fecha__month=mes,fecha__day=dia)[0].numero_entradas
    #reservado=round(((reservado*100)/total_entradas),2)
    #normal=round(((normal*100)/total_entradas),2)
    no_vendidas=total_entradas-reservado-normal
    return no_vendidas,normal,reservado

