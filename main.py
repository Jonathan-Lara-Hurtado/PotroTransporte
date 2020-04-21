import datetime

def aumentarDias(fecha,d):
    return fecha+datetime.timedelta(days=d)

inicio = datetime.date.today()+datetime.timedelta()
print(inicio)

def dias(date,d):
    fecha = aumentarDias(date,1)
    a=1
    fechaInicial = date
    while a <= d:
        if fecha.strftime("%A")=="Saturday":
            fecha = aumentarDias(fecha,2)
        elif fecha.strftime("%A") == "Sunday":
            fecha = aumentarDias(fecha, 1)
        else:
            if a < 2:
                fechaInicial = fecha
                a = a + 1
            else:
                fecha = aumentarDias(fecha, 1)
                a=a+1

    return [fechaInicial,fecha]