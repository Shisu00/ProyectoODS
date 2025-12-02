from django.urls import path, include
from . import views
from .api_views import ProductoList

app_name = 'rescateComida'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    
    path('cliente/dashboard/', views.dashboard_cliente, name='dashboard_cliente'),
    path('cliente/proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('cliente/proveedor/<int:proveedor_id>/', views.proveedor_perfil, name='proveedor_perfil'),
    path('cliente/producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    path('cliente/perfil/', views.perfil_cliente, name='perfil_cliente'),
    
    path('proveedor/dashboard/', views.dashboard_proveedor, name='dashboard_proveedor'),
    path('proveedor/producto/crear/', views.producto_crear, name='producto_crear'),
    path('proveedor/producto/editar/<int:producto_id>/', views.producto_editar, name='producto_editar'),
    path('proveedor/producto/eliminar/<int:producto_id>/', views.producto_eliminar, name='producto_eliminar'),
    path('proveedor/perfil/', views.perfil_proveedor, name='perfil_proveedor'),

    path('carrito/', views.ver_carrito, name='carrito'),
    path('carrito/agregar/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/finalizar/', views.finalizar_compra, name='finalizar_compra'),

    path('admin/', include('adminpanel.urls')),
    path('api/productos/', ProductoList.as_view(), name='api_productos'),
    #path('api/external/', api_externa, name='api_externa'),
]
