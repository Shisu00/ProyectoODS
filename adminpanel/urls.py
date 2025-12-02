from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
]
