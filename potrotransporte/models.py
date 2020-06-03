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
    #Nombre = models.CharField(max_length=20,default="")
    PKUsuario = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    Licencia = models.CharField(max_length=20,default="")
    telefono = models.CharField(max_length=15,default="")
    Dirrecion = models.CharField(max_length=20,default="")

    def __str__(self):
        return str(self.PKUsuario.first_name)


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



class RutaReserva(models.Model):
    EstadoReserva = (
        ('P', 'Reservado'),
        ('C', 'Cancelado'),
    )

    turnoEscolar = (
        ('M','Matutino'),
        ('V','Vespertino'),
    )

    UsuarioFK = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    RutaFk = models.ForeignKey(Ruta,on_delete=models.CASCADE,default="")
    fechaRegistro = models.DateField(_("Fecha"),default=datetime.date.today)
    estadoReserva = models.CharField(max_length=1, choices=EstadoReserva, default='C')
    turno = models.CharField(max_length=1,choices=turnoEscolar,default='M')

    def __str__(self):
        return str(self.UsuarioFK)


class Asistencia(models.Model):

    ReservaFK = models.ForeignKey(RutaReserva,on_delete=models.CASCADE,default="")
    ida = models.BooleanField(default=False)
    vuelta = models.BooleanField(default=False)
    rutaFK = models.ForeignKey(Ruta,on_delete=models.CASCADE,default=1)
    fechaDeIda = models.DateTimeField(_("Fecha"),default=(datetime.date.today() +datetime.timedelta(days=1)))
    fechaVuelta = models.DateTimeField(_("Fecha"),default=(datetime.date.today() +datetime.timedelta(days=1)))

    def __str__(self):
        return str(self.fechaReserva)



class TipoMembresias(models.Model):
    Duracion = (
        ('S', 'Semanal'),
        ('M', 'Mensual'),
        ('C', 'Trimestral'),
    )
    Nombre = models.CharField(max_length=40)
    costo = models.IntegerField()
    duracion = models.CharField(max_length=1, choices=Duracion, default='C')
    costoPorDuracion = models.IntegerField(default=0)

    def __str__(self):
        return self.Nombre


class Membresia(models.Model):
    EstadoPago = (
        ('P', 'Pagado'),
        ('C', 'Cancelado'),
        ('E', 'Pendiente'),
        ('T', 'Cancelado Tiempo'),
        ('W', 'Expiro Membresia')
    )

    UsuarioFk = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    MembresiaFk = models.ForeignKey(TipoMembresias, on_delete=models.CASCADE,default="")
    FechaCreacion = models.DateField(_("Fecha creacion"),default=datetime.date.today)
    EstadoPago = models.CharField(max_length=1, choices=EstadoPago, default='E')

class DetallePagoMembresia(models.Model):

    MembresiaFK = models.ForeignKey(Membresia,on_delete=models.CASCADE,blank=False)
    FechaInicio = models.DateField(_("Fecha Inicio"),default=datetime.date.today)
    FechaTerminacion = models.DateField(_("Fecha Terminacion"),default=datetime.date.today)
    FechaAprobacion = models.DateField(_("Fecha Aprobacion"),default=datetime.date.today)
    administrativoFK = models.ForeignKey(User,on_delete=models.CASCADE,default="")


class Avisos(models.Model):
    titulo = models.CharField(max_length=30,blank=False)
    mensaje = models.CharField(max_length=30,blank=False)
    admin = models.ForeignKey(User,on_delete=models.CASCADE,blank=False)
    fechaCreacion = models.DateField(_("Fecha"),default=datetime.date.today)
