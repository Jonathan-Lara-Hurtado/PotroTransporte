from django.shortcuts import render
from django.views.generic import RedirectView
from .forms import *
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
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
from .templatetags.auth_extras import has_group
from django.core import serializers

class MembresiaHerramienta:

    def fechaHoy(self):
        return datetime.date.today()

    def aumentarDias(self, fecha, d):
        return fecha + datetime.timedelta(days=d)

    def dias(self, date, d):
        fecha = self.aumentarDias(date, 1)
        a = 1
        fechaInicial = date
        while a <= d:
            if fecha.strftime("%A") == "Saturday":
                fecha = self.aumentarDias(fecha, 2)
            elif fecha.strftime("%A") == "Sunday":
                fecha = self.aumentarDias(fecha, 1)
            else:
                if a < 2:
                    fechaInicial = fecha
                    a = a + 1
                else:
                    fecha = self.aumentarDias(fecha, 1)
                    a = a + 1

        return [fechaInicial, fecha]


class VistaPrincipal(RedirectView):

    def get(self, request, *args, **kwargs):
        rutas = Ruta.objects.all()
        formMembresia = FormularioMembresia()
        listaMembresia= TipoMembresias.objects.all()
        self.cancelarPagosRetrasados(request.user)
        membresia = self.MembresiaActivaoPendiente(request.user)
        listaAvisos = self.listasAvisos()
        return render(request, 'potrotransporte/index.html', {"membresia":membresia,
                                                              "rutas":rutas,
                                                              "FormMembresia":formMembresia,
                                                              "listaMembresia":listaMembresia,
                                                              "listaAvisos":listaAvisos})

    def post(self, request, *args, **kwargs):
        print(request.POST['Respuesta'])
        user = User.objects.get(pk=request.user.pk)
        if request.POST['Respuesta'] == "addAnuncio":
            admob = Avisos()
            admob.titulo = request.POST['titulo']
            admob.mensaje = request.POST['mensaje']
            admob.admin = user
            admob.save()
        return JsonResponse({"message": "Cambio realizado con exitoso"}, status=201)

    def listasAvisos(self):
        m = Avisos.objects.filter(fechaCreacion__month='04')
        return m
    def cancelarPagosRetrasados(self,r):
        lista = Membresia.objects.filter(UsuarioFk=r.pk)
        for i in lista:
            if i.EstadoPago == 'E':
                dia = self.dias_diferencia(i.FechaCreacion,datetime.date.today())
                print("diassssss:"+str(dia))
                if dia > 7:
                    f = Membresia.objects.get(pk=i.pk)
                    f.EstadoPago = 'T'
                    f.save()

    def MembresiaActivaoPendiente(self,r):
        lista = Membresia.objects.filter(UsuarioFk=r.pk)
        for i in lista:
            if i.EstadoPago == 'E' or i.EstadoPago == 'P':
                return i

    def dias_diferencia(self,dv,dn):
        return abs(dn-dv).days


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
                'uid': urlsafe_base64_encode(force_bytes(f.pk)),
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
                'uid': urlsafe_base64_encode(force_bytes(f.pk)),
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
        return HttpResponse('Su cuenta ha sido activada exitosamente <br><a href="https://jonabimael.pythonanywhere.com/potrotransporte/acceso/">Acceso</a>')
    else:
        return HttpResponse('Su cuenta ha sido activada exitosamente <br><a href="https://jonabimael.pythonanywhere.com/potrotransporte/acceso/">Acceso</a>')
        #return HttpResponse('¡El enlace de activación no es válido!')
        #

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

        if has_group(user=request.user,group_name="Administrativos"):
            return self.render_to_response({'form': self.form,
                                            'rutas': rutas,
                                            'form2': self.form2,
                                            'form3': self.form3,
                                            'ListaOperador': operador,
                                            'ListaTransporte': transporte
                                            })
        else:
            return redirect('/')



    def post(self, resquest):
        if has_group(user=resquest.user, group_name="Administrativos"):
            Resultado = resquest.POST['Resultado']
            if Resultado == "Operador":
                g_Operadores, operadored = Group.objects.get_or_create(name='Operadores')
                f = User.objects.create_user(resquest.POST['Correo'],
                                             resquest.POST['Correo'],
                                             resquest.POST['Contrasena'])
                f.first_name = resquest.POST['Nombre']
                f.last_name = resquest.POST['Apellidos']
                f.is_active = True
                f.groups.add(g_Operadores)
                f.save()
                m = Operador()
                m.PKUsuario = User.objects.get(pk=f.pk)
                m.Licencia = resquest.POST['Licencia']
                m.telefono = resquest.POST['Telefono']
                m.Dirrecion = resquest.POST['Direccion']
                m.save()
                return redirect('/')
            else:
                form = FormularioCrearRuta(resquest.POST)
                if form.is_valid():
                    f = Ruta()
                    f.NombreRuta = form.data['NombreRuta']
                    f.Horario=form.data['Horario']
                    f.Latitud=form.data['Latitud']
                    f.Longitud=form.data['Longitud']
                    f.TransporteFK = Transporte.objects.get(pk= form.data['Transporte'])
                    f.save()
                    return redirect('/')
                else:
                    return HttpResponse("error al agregar ruta")
        else:
            return redirect('/')


class VistaHistorialCobro(LoginRequiredMixin,TemplateView):

    template_name = "potrotransporte/historialmembresias.html"

    def get(self, request, *args, **kwargs):
        usuario= User.objects.get(pk=request.user.pk)
        Historial = Membresia.objects.filter(UsuarioFk=usuario)
        return self.render_to_response({'Historial':Historial})

class LazyEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, DetallePagoMembresia):
            return str(o)
        return super().default(o)

class VistaHistorialData(LoginRequiredMixin,TemplateView):

    def get(self,request):
        usuario= User.objects.get(pk=request.user.pk)
        Historial = Membresia.objects.filter(UsuarioFk=usuario)
        post_list = serializers.serialize('json',Historial,cls=LazyEncoder)
        print(post_list)
        d = json.loads(post_list)
        return JsonResponse(d, safe=False)

class VistaCobro(LoginRequiredMixin,TemplateView):

    template_name = "potrotransporte/cobrotransporte.html"

    def get(self, request, *args, **kwargs):
        formularioTiposCobro = FormularioTiposCobro()
        listaCobros = self.listaApagar()
        return self.render_to_response({'formularioTiposCobro': formularioTiposCobro,
                                        'listaCobros':listaCobros,
                                        })

    def post(self, resquest):
        print(resquest.POST['Respuesta'])
        if resquest.POST['Respuesta'] == "Activacion":
            self.activacion(resquest)
            return JsonResponse({"message": "Cambio realizado con exitoso"}, status=201)
        elif resquest.POST['Respuesta'] == "Cancelacion":
            self.cancelacion(resquest)
            return JsonResponse({"message": "Cambio realizado con exitoso"}, status=201)
        elif resquest.POST['Respuesta'] == "Pago":
            self.pago(resquest)
            return JsonResponse({"message": "Cambio realizado con exitoso"}, status=201)
        elif resquest.POST['Respuesta']:
            self.agregarMembresia(resquest)
            return JsonResponse({"message": "Cambio realizado con exitoso"}, status=201)
        else:
            return JsonResponse({"message": "error"}, status=201)

    def activacion(self,r):
        usuario = User.objects.get(pk=r.user.pk)
        mebresia = TipoMembresias.objects.get(duracion=r.POST['ValSelect'])
        f = Membresia()
        f.UsuarioFk = usuario
        f.MembresiaFk = mebresia
        f.EstadoPago = 'E'
        f.save()

    def cancelacion(self,r):
        m = Membresia.objects.get(pk=r.POST['idMembresia'])
        m.EstadoPago = 'C'
        m.save()

    def listaApagar(self):
        l = Membresia.objects.filter(EstadoPago='E')
        return l

    def pago(self,r):
        print(r.POST)
        m = Membresia.objects.get(pk=r.POST['idMembresia'])
        print(m.MembresiaFk.duracion)
        if m.MembresiaFk.duracion == 'C':
            self.generarDetallesMembresia(r, m , 30*3)
        elif m.MembresiaFk.duracion == 'M':
            self.generarDetallesMembresia(r, m, 30)
        else:
            self.generarDetallesMembresia(r, m, 5)

    def generarDetallesMembresia(self, r, m,cDia):
        MHObj = MembresiaHerramienta()
        fecha = MHObj.dias(MHObj.fechaHoy(), cDia)
        m.EstadoPago = 'P'
        userAdmin = User.objects.get(pk=r.user.pk)
        detallesMembresia = DetallePagoMembresia()
        detallesMembresia.MembresiaFK = m
        detallesMembresia.administrativoFK = userAdmin
        detallesMembresia.FechaInicio = fecha[0]
        detallesMembresia.FechaTerminacion =fecha[1]
        detallesMembresia.FechaAprobacion = MHObj.fechaHoy()
        detallesMembresia.save()
        m.save()


    def agregarMembresia(self,r):
        m = TipoMembresias()
        m.Nombre = r.POST['nombre']
        m.costo =r.POST['CostodelPasaje']
        m.duracion = r.POST['Duracion']
        m.costoPorDuracion = r.POST['CostoMembresia']
        m.save()


class VistaAsistencia(LoginRequiredMixin,TemplateView):
    template_name = "potrotransporte/Asistencia.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'lista':'l'}, content_type="text/html; charset=utf-8")


class VistaReservaAsistencia(LoginRequiredMixin,TemplateView):

    template_name = "potrotransporte/Reserva.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'l': 'l'})