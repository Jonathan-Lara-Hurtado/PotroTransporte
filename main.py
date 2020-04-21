import datetime
from dateutil.rrule import DAILY,rrule,MO,TU,WE,TH,FR
def fechaRango(inicioFe,finalFec):
    return rrule(DAILY,dtstart=inicioFe,until=finalFec,byweekday=(MO,TU,WE,TH,FR))


p = datetime.datetime.now() + datetime.timedelta(days=1)
d = datetime.date.today() +datetime.timedelta(days=1)
inicio = datetime.date.today()+datetime.timedelta(days=4)
final = datetime.date.today() +datetime.timedelta(days=6)
#print(final.strftime("%A"))


def diaHabil(date):
    if date.strftime("%A") == "Saturday" or date.strftime("%A") == "Sunday":
        return False
    else:
        return True

def aumentarDias(fecha,d):
    return fecha+datetime.timedelta(days=d)

def semana(fechaAprobacion):
    fechaInicio = aumentarDias(fechaAprobacion, d=1)
    print(fechaInicio)
    if diaHabil(fechaInicio):
        pass
    else:
        if fechaInicio.strftime("%A") == "Saturday":
            fechaInicio = aumentarDias(fechaAprobacion, d=3)
            print(fechaInicio)
        else:
            fechaInicio = aumentarDias(fechaAprobacion, d=2)
            print(fechaInicio)


semana(inicio)