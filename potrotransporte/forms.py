from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.contrib.auth.hashers import PBKDF2SHA1PasswordHasher, SHA1PasswordHasher,check_password
from .models import Transporte,Operador,TipoMembresias,Ruta

class FormularioMembresia(forms.Form):
    membresia = forms.ModelChoiceField(queryset=TipoMembresias.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))


class FormularioReserva(forms.Form):
    pass

class FormularioTiposCobro(forms.Form):
    Duracion = (
        ('S', 'Semanal'),
        ('M', 'Mensual'),
        ('C', 'Trimestral'),
    )
    Nombre = forms.CharField(label="Nombre:",help_text="Nombre relacionado con la duracion de la membresia")
    costo = forms.IntegerField(label="Costo del pasaje",widget=forms.NumberInput(attrs={'class':"form-control",
                                                                                        'id':"costo",
                                                                                        'onchange':"calcularCosto()"}))
    duracion = forms.ChoiceField(choices=Duracion,widget=forms.Select(attrs={'class':'form-control',
                                                                             'id':'duracionSelect',
                                                                             'onchange':"calcularCosto()"}))
    costoPorDuracion = forms.IntegerField(label="Costo de la membresia",widget=forms.NumberInput(attrs={'class':"form-control",
                                                                                                        'id':'precioFinal'}))

    Nombre.widget = forms.TextInput(attrs={'class': "form-control"})

    costoPorDuracion.widget.attrs['readonly'] = True

class Registro(forms.Form):

    your_names = forms.CharField(label=_('Nombres:'), max_length=100)
    your_last_names = forms.CharField(label=('Apellidos'),max_length=100)
    your_email = forms.EmailField(label=_('Correo Electronico'), required=True)
    your_password = forms.CharField(label=_('Contraseña'),widget=forms.PasswordInput,required=True)
    repeat_password = forms.CharField(label=_('Repetir Contraseña'),widget=forms.PasswordInput,required=True)


    your_names.widget =forms.TextInput(attrs={'class':"form-control"})
    your_last_names.widget = forms.TextInput(attrs={'class':"form-control"})
    your_email.widget = forms.TextInput(attrs={'class':"form-control",'type':"email"})
    your_password.widget = forms.TextInput(attrs={'class':"form-control",'type':"password"})
    repeat_password.widget = forms.TextInput(attrs={'class':"form-control",'type':"password"})

    def clean(self):
        limpiar_Datos = super(Registro,self).clean()
        password = limpiar_Datos.get("your_password")
        confirm_password = limpiar_Datos.get("repeat_password")
        username = limpiar_Datos.get("your_email")
        correo = limpiar_Datos.get("your_email")

        if not self.ValidacionCorreoInstitucional(correo):
            raise forms.ValidationError(u'El correo electronico no es Institucional debe ser de la siguiente forma @alumno.uaemex.mx o @profesor.uaemex.mx')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(u'El correo electronico ya esta en uso')
        else:
            if password != confirm_password:
                raise forms.ValidationError(
                    "Las contraseña no coinciden"
                )

    def ValidacionCorreoInstitucional(self,correo):
        c = correo.split("@")
        if c[1] == "profesor.uaemex.mx" or c[1] == "alumno.uaemex.mx":
            return True
        else:
            return False



class Acceso(forms.Form):
    your_email = forms.EmailField(label=_('Correo Electronico'), required=True)
    your_email.widget = forms.TextInput(attrs={'class':"form-control",'type':"email"})
    your_password = forms.CharField(label=_('Contraseña'), widget=forms.PasswordInput, required=True)
    your_password.widget =forms.TextInput(attrs={'class':"form-control",'type':"password"})
    intentos = 0

    def clean(self):
        limpiar_Datos = super(Acceso, self).clean()
        username = limpiar_Datos.get("your_email")
        passwordform = limpiar_Datos.get("your_password")
        user = User.objects.filter(username=username)
        if user.exists():
            cifrado =User.objects.get(username=username).password
            if not check_password(passwordform,cifrado):
                self.intentos +=1
                print(self.intentos)
                raise forms.ValidationError(u'Contraseña Incorrecta')
        else:
            raise forms.ValidationError(u'El Usuario no esta registrado')

class FormularioCrearRuta(forms.Form):

    NombreRuta = forms.CharField(label="Nombre ruta:",max_length=30)
    Horario = forms.CharField(label="Nombre ruta:",max_length=30)
    Latitud = forms.FloatField(required=True,widget=forms.NumberInput(attrs={'class':"form-control", 'step': "0.0000000000000001"}))
    Longitud = forms.FloatField(required=True,widget=forms.NumberInput(attrs={'class':"form-control", 'step': "0.0000000000000001"}))
    Transporte = forms.ModelChoiceField(queryset=Transporte.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))

    NombreRuta.widget =forms.TextInput(attrs={'class':"form-control"})
    Horario.widget =forms.TextInput(attrs={'class':"form-control"})



class FormularioCrearOperadores(forms.Form):
    Correo = forms.CharField(label="Correo: ",max_length=20)
    Contrasena = forms.CharField(label=_('Contraseña'), widget=forms.PasswordInput, required=True)
    Nombre = forms.CharField(label="Nombres:",max_length=20)
    Apellidos = forms.CharField(label="Apellidos:",max_length=20)
    Licencia = forms.CharField(label="licencia",max_length=20)
    Telefono = forms.CharField(label="Telefono",max_length=15)
    Direccion = forms.CharField(label="Dirreccion",max_length=20)

    Correo.widget = forms.TextInput(attrs={'class':"form-control"})
    Contrasena.widget = forms.TextInput(attrs={'class':"form-control",'type':"password"})
    Nombre.widget=forms.TextInput(attrs={'class':"form-control"})
    Apellidos.widget=forms.TextInput(attrs={'class':"form-control"})
    Licencia.widget=forms.TextInput(attrs={'class':"form-control"})
    Telefono.widget=forms.TextInput(attrs={'class':"form-control"})
    Direccion.widget=forms.TextInput(attrs={'class':"form-control"})

class FormularioTransporte(forms.Form):
    Nombre = forms.CharField(label="Nombre:",max_length=20)
    Tipo = forms.CharField(label="Tipo:",max_length=20)
    Matricula = forms.CharField(label="Matricula:",max_length=20)
    OperadorFk = forms.ModelChoiceField(label="Operador",queryset=Operador.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))


    Nombre.widget=forms.TextInput(attrs={'class':"form-control"})
    Tipo.widget=forms.TextInput(attrs={'class':"form-control"})
    Matricula.widget=forms.TextInput(attrs={'class':"form-control"})


class FormularioReserva(forms.Form):
    turnoEscolar = (
        ('M', 'Matutino'),
        ('V', 'Vespertino'),
    )
    turno = forms.ChoiceField(label="Turno:",choices=turnoEscolar,widget=forms.Select(attrs={'class':'form-control'}))
    RutaFK= forms.ModelChoiceField(label="Ruta",queryset=Ruta.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))