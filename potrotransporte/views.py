from django.shortcuts import render
from django.views.generic import RedirectView
from .forms import *
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


#librerias de autentificacion
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError,send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .token_generator import account_activation_token
from smtplib import SMTPException
from django.contrib.auth import login, authenticate,logout
from django.shortcuts import redirect
from .models import *
from django.contrib.auth.models import Group,Permission

class VistaPrincipal(RedirectView):

    def get(self, request, *args, **kwargs):
        rutas = Ruta.objects.all()
        return render(request, 'potrotransporte/index.html', {"gato":"gg",
                                                              "rutas":rutas})


class VistaRegistroAdmin(RedirectView):

    form = Registro()

    def get(self, request, *args, **kwargs):
        if request.user.username != "":
            username = request.user.username
            password = request.user.password
            user = authenticate(request, username=username, password=password)
            if user is None:
                return redirect('/')
            else:
                return render(request, 'potrotransporte/registroAdministrativo.html', {"form": self.form})
        return render(request, 'potrotransporte/registroAdministrativo.html', {"form": self.form})


    def post(self, request, *args, **kwargs):
        form = Registro(request.POST)
        if form.is_valid():
            g_administrativos, administrativos = Group.objects.get_or_create(name='Administrativos')
            f = User.objects.create_user(form.data['your_email'],
                                         form.data['your_email'],
                                         form.data['your_password'])
            f.first_name = form.data['your_names']
            f.last_name = form.data['your_last_names']
            f.is_active = False
            f.groups.add(g_administrativos)
            f.save()
            current_site = get_current_site(request)
            email_subject = 'Activacion de Cuenta'
            message = render_to_string('potrotransporte/activate_account.html', {
                'user': f,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(f.pk)).decode(),
                'token': account_activation_token.make_token(f),
            })
            to_email = form.cleaned_data.get('your_email')
            email = EmailMessage(email_subject, message, to=[to_email])
            print(email.send())
            return HttpResponse(
                'Le hemos enviado un correo electrónico, confirme su dirección de correo electrónico para completar el registro.')
        else:
            return render(request, "potrotransporte/registro.html", {'form': form})


# Create your views here.
class VistaRegistro(RedirectView):

    form = Registro()

    def get(self, request, *args, **kwargs):
        if request.user.username != "":
            username = request.user.username
            password = request.user.password
            user = authenticate(request, username=username, password=password)
            if user is None:
                return redirect('/')
            else:
                return render(request, 'potrotransporte/registro.html', {'form': self.form})
        else:
            return render(request, 'potrotransporte/registro.html', {"form": self.form})

    def post(self, request, *args, **kwargs):
        form = Registro(request.POST)
        if form.is_valid():
            g_usuarios, usuarios = Group.objects.get_or_create(name='Usuarios')
            f = User.objects.create_user(form.data['your_email'],
                          form.data['your_email'],
                          form.data['your_password'])
            f.first_name = form.data['your_names']
            f.last_name = form.data['your_last_names']
            f.is_active = False
            f.groups.add(g_usuarios)
            f.save()

            current_site = get_current_site(request)
            email_subject = 'Activacion de Cuenta'
            message = render_to_string('potrotransporte/activate_account.html', {
                'user': f,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(f.pk)).decode(),
                'token': account_activation_token.make_token(f),
            })
            to_email = form.cleaned_data.get('your_email')
            email = EmailMessage(email_subject, message, to=[to_email])
            print(email.send())
            return HttpResponse('Le hemos enviado un correo electrónico, confirme su dirección de correo electrónico para completar el registro.')
        else:
            return render(request, "potrotransporte/registro.html", {'form': form})


class VistaDesconectar(RedirectView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')

    def post(self, request, *args, **kwargs):
        logout(request)
        redirect('/')


class VistaAcceso(RedirectView):
    form = Acceso()

    def get(self, request, *args, **kwargs):
        if request.user.username != "":
            username = request.user.username
            password = request.user.password
            user = authenticate(request, username=username, password=password)
            if user is None:
                return redirect('/')
            else:
                return render(request, 'potrotransporte/acceso.html', {'form': self.form})
        else:
            return render(request, 'potrotransporte/acceso.html', {'form': self.form})


    def post(self, request, *args, **kwargs):
        formulario = Acceso(request.POST)
        username = formulario.data['your_email']
        password = formulario.data['your_password']
        user = authenticate(request, username=username, password=password)
        if formulario.is_valid():
            if user is not None:
                login(request, user)
                return redirect('/')
#                return render(request, 'potrotransporte/index.html', {'user': user})
        else:
            return render(request, "potrotransporte/acceso.html", {'form': formulario})




def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Su cuenta ha sido activada exitosamente')
    else:
        return HttpResponse('¡El enlace de activación no es válido!')


class VistaDatos(LoginRequiredMixin,TemplateView):
    template_name = 'potrotransporte/datos.html'
    login_url = 'acceso'

    def get(self, request):
        return self.render_to_response({})


class VistaAgregarRuta(LoginRequiredMixin,TemplateView):
    template_name = "potrotransporte/crear_ruta.html"
    login_url = 'acceso'
    form = FormularioCrearRuta()
    form2 = FormularioCrearOperadores()
    form3 = FormularioTransporte()


    def get(self, request, *args, **kwargs):
        rutas = Ruta.objects.all()
        operador = Operador.objects.all()
        transporte = Transporte.objects.all()

        return self.render_to_response({'form': self.form,
                                        'rutas':rutas,
                                        'form2':self.form2,
                                        'form3':self.form3,
                                        'ListaOperador':operador,
                                        'ListaTransporte':transporte
                                        })

    def post(self, resquest):
        print(resquest.POST)
        form = FormularioCrearRuta(resquest.POST)
        if form.is_valid():
            f = Ruta()
            f.NombreRuta = form.data['NombreRuta']
            f.Horario=form.data['Horario']
            f.Latitud=form.data['Latitud']
            f.Longitud=form.data['Longitud']
            f.save()
            return redirect('/')
        else:
            return HttpResponse("error al agregar ruta")