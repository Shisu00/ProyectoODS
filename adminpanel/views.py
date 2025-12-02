from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rescateComida.models import Usuario, Producto, Transaccion
from rescateComida.decorators import role_required
from rescateComida.forms import RegistroForm

#DASHBOARD
@role_required('admin')
def dashboard_admin(request):
    context = {
        'total_usuarios': Usuario.objects.count(),
        'total_productos': Producto.objects.count(),
        'total_transacciones': Transaccion.objects.count(),
        'usuarios_por_tipo': {
            'clientes': Usuario.objects.filter(tipo_usuario='cliente').count(),
            'proveedores': Usuario.objects.filter(tipo_usuario='proveedor').count(),
            'admins': Usuario.objects.filter(tipo_usuario='admin').count(),
        }
    }
    return render(request, 'adminpanel/dashboard_admin.html', context) 

##### CRUD ######
#LISTAR USUARIOS
@role_required('admin')
def lista_usuarios(request):
    usuarios = Usuario.objects.all().order_by('-date_joined')
    return render(request, 'adminpanel/lista_usuarios.html', {'usuarios': usuarios})

#BOTON CREAR USUARIO
@role_required('admin')
def crear_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuario {usuario.username} creado como {usuario.get_tipo_usuario_display()}')
            return redirect('adminpanel:lista_usuarios')
    else:
        form = RegistroForm(initial={'tipo_usuario': 'cliente'})  # Valor por defecto
    
    return render(request, 'adminpanel/formUsuario.html', {'form': form, 'accion': 'Crear'})

#EDITAR
@role_required('admin')
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == 'POST':
        form = RegistroForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuario {usuario.username} actualizado exitosamente')
            return redirect('adminpanel:lista_usuarios')
    else:
        form = RegistroForm(instance=usuario)
    
    return render(request, 'adminpanel/formUsuario.html', {'form': form, 'accion': 'Editar', 'usuario': usuario})

#ELIMINAR
@role_required('admin')
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == 'POST':
        username = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario {username} eliminado exitosamente')
        return redirect('adminpanel:lista_usuarios')
    
    return render(request, 'adminpanel/confirmarEliminar.html', {'usuario': usuario})
