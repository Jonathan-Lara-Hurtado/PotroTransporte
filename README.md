###############################################MercadoLnd#######################################################


##########################################################################################
#	Requisitos
#-mysql(sudo apt-get install mysql-server)
#
#Prerequisites para el conector mysqlclient de python
#-sudo apt-get install python-dev default-libmysqlclient-dev
#  
#     pip3 install -r requerimientos.txt
#-django
#-django-countries
#-django-summernote
#-mysqlclient
#-django-stdimage
#-SSL CERT https://github.com/teddziuba/django-sslserver
##########################################################################################
pip install django-qr-code



##########################################################################################
#ejecutar por primera vez la aplicacion
#python3 manage.py
#python3 manage.py migrate
#python3 manage.py makemigrations mercadoln
##########################################################################################


##########################################################################################
#diferente formas de ejecutar la aplicacion
#python manage.py runserver <direccion>:<puerto>
#python manage.py runserver <puerto>
#Nota:la direccion se configura en mercadolnd/settings.py en ALLOWED_HOSTS = [<direccion>]
#     ,puede estar este sin direccion y por defecto tomara la ip de localhost 127.0.0.1
#
#
#Es este caso conforme a nuesto archivo settings.py la direccion es 192.168.1.79 entonces
#para corre el programa seria el siguiente comando
#
#-python3 manage.py runserver 0.0.0.0:8001
##########################################################################################



##########################################################################################
#creacion de un superusuario root en django aplicacion
python3 manage.py createsuperuser


#CREACION DE MODELO GRAFICO
sudo apt install libgraphviz-dev x
pip3 install pygraphviz
pip install django-extensions pygraphviz


INSTALLED_APPS = [ 
                   ...
                   'django_extensions',
]
#ALERT while copying: inverted comma in medium is different

python3 manage.py graph_models -a > modelo.dot

#To group all the application and output into PNG file
$ python manage.py graph_models -a -g -o imagefile_name.png#Include only some applications
$ python manage.py graph_models app1 app2 -o app1_app2.png#Include only some specific models
$ python manage.py graph_models -a -I Foo,Bar -o foo_bar.png#OR exclude certain models 
$ python manage.py graph_models -a X Foo,Bar -o no_foo_bar.png