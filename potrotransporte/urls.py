from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
path('', views.VistaPrincipal.as_view(), name='index'),
path('registroadmin/', views.VistaRegistroAdmin.as_view(), name='registroadmin'),
path('registro/', views.VistaRegistro.as_view(), name='registro'),
url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_account, name='activate'),
path('desconectar/',views.VistaDesconectar.as_view(),name='desconectar'),
path('acceso/', views.VistaAcceso.as_view(), name='acceso'),
path('password-reset/', auth_views.PasswordResetView.as_view(template_name="potrotransporte/password_reset_email.html"), name='password_reset'),
path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="potrotransporte/password_reset_done.html"), name='password_reset_done'),
path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
path('datos/', views.VistaDatos.as_view(), name='datos'),
path('crear_ruta/', views.VistaAgregarRuta.as_view(), name='crear_ruta'),
path('cobro_transporte/', views.VistaCobro.as_view(), name='cobro_transporte'),
]


