from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Categoria, Producto, Transaccion, Valoracion


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Admin personalizado para Usuario"""
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'is_active']
    list_filter = ['tipo_usuario', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Información Adicional', {'fields': ('tipo_usuario', 'telefono', 'direccion', 'comuna')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'tipo_usuario'),
        }),
    )
    
    ordering = ['-date_joined']


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id_categoria', 'nombre_categoria']
    search_fields = ['nombre_categoria']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id_producto', 'nombre', 'id_usuario', 'id_categoria', 'estado', 'fecha_publicacion']
    list_filter = ['estado', 'fecha_publicacion', 'id_categoria']
    search_fields = ['nombre', 'id_usuario__username']
    readonly_fields = ['fecha_publicacion']


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ['id_transaccion', 'id_producto', 'id_cliente', 'tipo', 'estado', 'fecha_solicitud']
    list_filter = ['tipo', 'estado', 'fecha_solicitud']
    search_fields = ['id_cliente__username', 'id_producto__nombre']
    readonly_fields = ['fecha_solicitud']


@admin.register(Valoracion)
class ValoracionAdmin(admin.ModelAdmin):
    list_display = ['id_valoracion', 'id_transaccion', 'id_usuario', 'puntuacion', 'fecha_valoracion']
    list_filter = ['puntuacion', 'fecha_valoracion']
    search_fields = ['id_usuario__username', 'id_transaccion__id_transaccion']
    readonly_fields = ['fecha_valoracion']
