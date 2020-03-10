from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import datetime
from django.utils.translation import gettext as _

class DatosPersonales(models.Model):
    NumeroDeCuenta = models.CharField(max_length=20,default="")
    Telefono = models.CharField(max_length=20,default="")
    TelefonoAlternativo = models.CharField(max_length=20,default="")
    TipoSangre = models.CharField(max_length=4,default="")
    Alergias = models.CharField(max_length=30,default="")
    DatoPersonalFk = models.ForeignKey(User,on_delete=models.CASCADE,default="")

    def __str__(self):
        return self.NumeroDeCuenta

class Operador(models.Model):
    Nombre = models.CharField(max_length=20,default="")
    Licencia = models.CharField(max_length=20,default="")
    telefono = models.CharField(max_length=15,default="")
    Dirrecion = models.CharField(max_length=20,default="")

    def __str__(self):
        return self.Nombre


class Transporte(models.Model):
    Nombre = models.CharField(max_length=10)
    Tipo = models.CharField(max_length=10)
    Matricula = models.CharField(max_length=10)
    OperadorFK = models.ForeignKey(Operador,on_delete=models.CASCADE,default="")

    def __str__(self):
        return self.Matricula

class Ruta(models.Model):
    NombreRuta = models.CharField(max_length=20,default="")
    Horario = models.CharField(max_length=30,default="")
    Latitud = models.FloatField()
    Longitud = models.FloatField()
    TransporteFK = models.ForeignKey(Transporte,on_delete=models.CASCADE,default="")

    def __str__(self):
        return self.NombreRuta


class Reserva(models.Model):
    UsuarioFK = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    RutaFk = models.ForeignKey(Ruta,on_delete=models.CASCADE,default="")
    fechaRegistro = models.DateField(_("Fecha"),default=datetime.date.today)

    def __str__(self):
        return str(self.UsuarioFK)



class Asistencia(models.Model):
    ReservaFK = models.ForeignKey(Reserva,on_delete=models.CASCADE,default="")
    ida = models.BooleanField(default=True)
    vuelta = models.BooleanField(default=True)
    fechaDeReserva = models.DateTimeField(_("Fecha"),default=(datetime.date.today() +datetime.timedelta(days=1)))

    def __str__(self):
        return str(self.fechaDeReserva)

class Pago(models.Model):
    Estados = (
        ('P', 'Pagado'),
        ('C', 'Cancelado'),
        ('E', 'Pendiente'),
        ('N', 'Nuevo'),
    )

    Membresias=(
        ('s', 'Semestral'),
        ('e', 'Semanal'),
        ('m', 'Mensual'),
    )

    UsuarioFK = models.ForeignKey(User,on_delete=models.CASCADE,default="")
    tipo = models.CharField(max_length=1,choices=Membresias,default='e')
    fechaCreacion = models.DateField(_("Fecha"),default=datetime.date.today)
    monto = models.FloatField(default=500)
    estatus = models.CharField(max_length=1,choices=Estados,default='N')


class AprobacionPago(models.Model):
    pagoFk = models.ForeignKey(Pago, on_delete=models.CASCADE, default="")
    fechaAprobacion = models.DateField(_("Fecha"),default=datetime.date.today)
    fechaExpiracion = models.DateField(_("Fecha"),default=datetime.datetime.today)
    UserAdministrativo = models.ForeignKey(User,on_delete=models.CASCADE,default="")