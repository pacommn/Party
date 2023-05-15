from django import forms
from .models import Discotecass, Usuarios,Fotos,Entradas
from django.core.validators import RegexValidator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class DiscotecasForm(forms.ModelForm):
    class Meta:
        model = Discotecass
        fields ='__all__'

class FotosForm(forms.ModelForm):

    class Meta:
        model = Fotos
        fields =('foto',)

    widgets = {
            'foto': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class EntradaForm(forms.ModelForm):
    dni = forms.CharField(validators=[RegexValidator(r'^\d{8}[A-Za-z]$', 'Ingrese un DNI válido.')])
    tipo = forms.ChoiceField(choices=(('N','Normal'),('R','Reservado')), widget=forms.Select,required=False, initial='N')
    correo_de_entrega=forms.CharField(required=False)
    class Meta:
        model = Entradas
        fields =('tipo','nombre','dni','cantidad','correo_de_entrega')
        


class UserForm(forms.ModelForm):
    #dni = forms.CharField(validators=[RegexValidator(r'^\d{8}[A-Za-z]$', 'Ingrese un DNI válido.')])
    contraseña = forms.CharField(validators=[RegexValidator(r'^(?=.*[0-9])', 'La contraseña debe contener al menos un número.')],widget=forms.PasswordInput)
    Repite_contraseña = forms.CharField(widget=forms.PasswordInput)
    #foto=forms.ImageField(required=False)
    class Meta:
        model = Usuarios
        fields =('usuario','correo')
        

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("contraseña")
        password_repeat = cleaned_data.get("Repite_contraseña")

        if password != password_repeat:
            self.add_error('Repite_contraseña', "Las contraseñas no coinciden.")

        #dni2 = cleaned_data.get("contrasena")
        #print(dni2)
        #if Usuarios.objects.filter(dni=dni2).exists():
            #self.add_error('dni', "Ya existe un usuario con ese DNI")

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=100)
    contrasena = forms.CharField(label="Contraseña", max_length=100, widget=forms.PasswordInput)

class UserForm2(forms.ModelForm):
    edad = forms.CharField(required=False)
    dni = forms.CharField(required=False) 

    class Meta:
        model = Usuarios
        fields = ('usuario', 'edad', 'dni', 'correo')

        