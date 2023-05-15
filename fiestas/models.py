from tabnanny import verbose
from django.db import models
from requests import delete


# Create your models here.


class Discotecass(models.Model):
    discotecaId=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=100,verbose_name="Nombre")
    foto= models.ImageField(upload_to='imagenes/',verbose_name="Foto de Perfil"  , null=True,max_length=200)
    direccion=models.CharField(max_length=500,verbose_name="direccion")
    descripcionp=models.CharField(max_length=1500,verbose_name="descripcion pequeña",null=True)
    descripciong=models.TextField(max_length=3000,verbose_name="descripcion grande",null=True)
    icono=models.ImageField(upload_to='imagenes/',verbose_name="Icono"  , null=True)
    

    def __str__(self):
        fila= "Nombre " + self.nombre + " - " + "direccion " + self.direccion   
        return fila

    def delete(self,using=None , keep_parent=False):
        self.foto.storage.delete(self.foto.name)
        super().delete()

class Usuarios(models.Model):
    usuarioId = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=100, verbose_name="Usuario", default='', unique=True)
    foto = models.ImageField(upload_to='imagenes/', verbose_name="Foto de Perfil", null=True,default='/media/imagenes/30995.jpg')
    edad = models.CharField(max_length=3, verbose_name="edad", default='', blank=True)
    dni = models.CharField(max_length=9, verbose_name="dni", default='', blank=True)
    correo = models.EmailField(max_length=100, verbose_name="correo", null=True, blank=True)
    contrasena = models.CharField(max_length=100, verbose_name="contraseña", null=False, default='')
    admin = models.IntegerField(verbose_name="admin", null=True)
    discotecaId = models.ForeignKey(Discotecass, null=True, on_delete=models.CASCADE)

    def __str__(self):
        fila= "Usuario " + self.usuario + " - " + "Correo " + self.correo
        return fila

class Fiestas(models.Model):
    fiestaId=models.AutoField(primary_key=True)
    foto= models.ImageField(upload_to='imagenes/',verbose_name="Foto de Perfil"  , null=True)
    descripcion=models.CharField(max_length=1500,verbose_name="descripcion")
    precio=models.IntegerField(verbose_name="precio")
    personas_reservado=models.IntegerField(verbose_name="Personas maxima del reservado")
    discotecaId=models.ForeignKey(Discotecass,null=True,on_delete=models.CASCADE)
    fecha=models.DateField(verbose_name="fecha")
    nombre=models.CharField(max_length=100,verbose_name="nombre")
    numero_entradas=models.IntegerField(verbose_name="numero de entradas")
    

    def __str__(self):
        fila= "Nombre " + self.nombre + " - " + "Fecha " + str(self.fecha)   
        return fila
    
class Carrito(models.Model):
    carritoId = models.AutoField(primary_key=True)
    usuarioId=models.ForeignKey(Usuarios,null=True,on_delete=models.CASCADE)

    def __str__(self):
        fila= "Id " + str(self.carritoId) 
        return fila
    
    def to_dict(self):
        return {
            'carritoId': self.carritoId,
            'usuarioId': self.usuarioId.usuarioId if self.usuarioId else None,
        }
    

class Entradas(models.Model):
    entradaId=models.AutoField(primary_key=True)
    tipo=models.CharField(max_length=20, choices=(('N','Normal'),('R','Reservado')) , default='N')
    coste=models.IntegerField(verbose_name="coste")
    dni=models.CharField(max_length=9, verbose_name="dni")
    nombre=models.CharField(max_length=100,verbose_name="nombre")
    cantidad=models.IntegerField(verbose_name="cantidad")
    personas=models.IntegerField(verbose_name="personas",null=True)
    fecha=models.DateField(verbose_name="fecha",blank=True, null=True,auto_now_add=True)
    discotecaId=models.ForeignKey(Discotecass,null=True,on_delete=models.CASCADE)
    fiestaId=models.ForeignKey(Fiestas,null=True,on_delete=models.CASCADE)
    usuarioId=models.ForeignKey(Usuarios,null=True,on_delete=models.CASCADE, blank=True)
    pagado=models.IntegerField(verbose_name="pagado",null=True)
    carritoId=models.ForeignKey(Carrito,null=True,on_delete=models.SET_NULL,blank=True)
    total = models.IntegerField(verbose_name="total", null=True)
    correo_de_entrega=models.CharField(max_length=100, verbose_name="correo de entrega",null=True)
    
    def __str__(self):
        fila= "Nombre " + self.nombre + " - " + "Dni " + self.dni   
        return fila
    
    def save(self, *args, **kwargs):
        self.total = self.cantidad * self.coste
        super(Entradas, self).save(*args, **kwargs)

class Fotos(models.Model):
    fotoId=models.AutoField(primary_key=True)
    foto= models.ImageField(upload_to='imagenes/',verbose_name="Foto"  , null=True)
    discotecaId=models.ForeignKey(Discotecass,null=True,on_delete=models.CASCADE)
    fecha=models.DateField(verbose_name="fecha",auto_now_add=True)

    def __str__(self):
        fila= "Discoteca " + self.discotecaId.nombre + " - " + "Fecha " + str(self.fecha)   
        return fila
    

class Subscripciones(models.Model):
    subscripcionId=models.AutoField(primary_key=True)
    discotecaId=models.ForeignKey(Discotecass,null=True,on_delete=models.CASCADE)
    usuarioId=models.ForeignKey(Usuarios,null=True,on_delete=models.CASCADE)

    def __str__(self):
        fila= "Discoetca " + self.discotecaId.nombre + " - " + "Usuario " + self.usuarioId.usuario  
        return fila



