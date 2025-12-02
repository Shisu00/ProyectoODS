from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .decorators import role_required
from .models import Usuario, Producto, Transaccion
from .forms import RegistroForm, LoginForm, ProductoForm, RegistroFormCliente
import json
from django.http import JsonResponse


def home(request):
    context = {
        'es_admin': request.user.is_authenticated and request.user.tipo_usuario == 'admin'
    }
    return render(request, 'home.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                usuario = Usuario.objects.get(username=username)
            except Usuario.DoesNotExist:
                try:
                    usuario = Usuario.objects.get(email__iexact=username)
                except Usuario.DoesNotExist:
                    messages.error(request, 'Usuario no encontrado')
                    return render(request, 'login.html', {'form': form})
            
            user = authenticate(request, username=usuario.username, password=password)
            
            if user is not None:
                login(request, user)  
                
                if user.tipo_usuario == 'proveedor':
                    return redirect('rescateComida:dashboard_proveedor')
                elif user.tipo_usuario == 'admin':
                    return redirect('adminpanel:dashboard_admin')
                else:
                    return redirect('rescateComida:dashboard_cliente')
            else:
                messages.error(request, 'Credenciales incorrectas')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def registro_view(request):
    if request.method == 'POST':
        form = RegistroFormCliente(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, 'Registro exitoso. Por favor inicia sesión.')
            return redirect('rescateComida:login')
    else:
        form = RegistroForm()
    
    return render(request, 'registro.html', {'form': form})

def logout_view(request):
    logout(request) 
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('rescateComida:home')




# ============== VISTAS DE CLIENTE ==============
@role_required('cliente')
def dashboard_cliente(request):
    productos = Producto.objects.filter(estado='disponible')
    return render(request, 'cliente/dashboard_cliente.html', {'productos': productos})


@role_required('cliente')
def lista_proveedores(request):
    proveedores = Usuario.objects.filter(tipo_usuario='proveedor')
    return render(request, 'cliente/lista_proveedores.html', {'proveedores': proveedores})


@role_required('cliente')
def proveedor_perfil(request, proveedor_id):
    proveedor = get_object_or_404(Usuario, id=proveedor_id, tipo_usuario='proveedor')
    productos = Producto.objects.filter(id_usuario=proveedor, estado='disponible')
    return render(request, 'cliente/proveedor_perfil.html', {
        'proveedor': proveedor,
        'productos': productos
    })


@role_required('cliente')
def producto_detalle(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    return render(request, 'cliente/producto_detalle.html', {'producto': producto})


@role_required('cliente')
def perfil_cliente(request):
    """Perfil del cliente"""
    usuario = request.user
    transacciones = Transaccion.objects.filter(id_cliente=usuario)
    co2_evitado = transacciones.count() * 0.5
    
    return render(request, 'cliente/perfil_cliente.html', {
        'usuario': usuario,
        'transacciones': transacciones,
        'co2_evitado': co2_evitado
    })


# ============== VISTAS DE PROVEEDOR ==============
@role_required('proveedor')
def dashboard_proveedor(request):
    productos = Producto.objects.filter(id_usuario=request.user)
    return render(request, 'proveedor/dashboard_proveedor.html', {'productos': productos})


@role_required('proveedor')
def producto_crear(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.id_usuario = request.user
            producto.save()
            messages.success(request, 'Producto creado exitosamente')
            return redirect('rescateComida:dashboard_proveedor')
    else:
        form = ProductoForm()
    
    return render(request, 'proveedor/producto_form.html', {'form': form, 'action': 'Crear'})


@role_required('proveedor')
def producto_editar(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id, id_usuario=request.user)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('rescateComida:dashboard_proveedor')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'proveedor/producto_form.html', {'form': form, 'action': 'Editar'})


@role_required('proveedor')
def producto_eliminar(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id, id_usuario=request.user)

    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente')
        return redirect('rescateComida:dashboard_proveedor')

    return render(request, 'proveedor/producto_confirmar_eliminar.html', {'producto': producto})


@role_required('proveedor')
def perfil_proveedor(request):
    usuario = request.user
    ventas = Transaccion.objects.filter(id_producto__id_usuario=usuario)
    productos_activos = usuario.productos.filter(estado='disponible').count()
    productos_publicados = usuario.productos.count()

    context = {
        'usuario': usuario,
        'ventas': ventas,
        'productos_activos': productos_activos,
        'productos_publicados': productos_publicados,
    }

    return render(request, 'proveedor/perfil_proveedor.html', context)


### CARRITO ###

@role_required('cliente')
def ver_carrito(request):
    """Ver contenido del carrito"""
    carrito = request.session.get('carrito', [])
    total = 0
    
    productos_en_carrito = []
    for item in carrito:
        producto = get_object_or_404(Producto, id_producto=item['producto_id'])
        subtotal = item['cantidad'] * producto.cantidad  # Asumiendo precio = cantidad
        total += subtotal
        
        productos_en_carrito.append({
            'producto': producto,
            'cantidad': item['cantidad'],
            'subtotal': subtotal
        })
    
    return render(request, 'cliente/carrito.html', {
        'productos': productos_en_carrito,
        'total': total,
        'carrito_items': len(carrito)
    })

@role_required('cliente')
def agregar_carrito(request):
    """Agregar producto al carrito via AJAX"""
    if request.method == 'POST':
        data = json.loads(request.body)
        producto_id = data['producto_id']
        cantidad = int(data['cantidad'])
        
        carrito = request.session.get('carrito', [])
        
        for item in carrito:
            if item['producto_id'] == producto_id:
                item['cantidad'] += cantidad
                request.session['carrito'] = carrito
                return JsonResponse({'success': True, 'total_items': len(carrito)})
        
        carrito.append({
            'producto_id': producto_id,
            'cantidad': cantidad
        })
        request.session['carrito'] = carrito
        
        return JsonResponse({'success': True, 'total_items': len(carrito)})
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@role_required('cliente')
def finalizar_compra(request):
    """Crear transacción desde carrito"""
    carrito = request.session.get('carrito', [])
    if not carrito:
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('rescateComida:dashboard_cliente')
    
    cliente = request.user
    
    for item in carrito:
        producto = get_object_or_404(Producto, id_producto=item['producto_id'])
        

        transaccion = Transaccion.objects.create(
            id_producto=producto,
            id_cliente=cliente,
            tipo='venta',
            estado='completada'
        )
        

        producto.estado = 'no_disponible'
        producto.save()
    
    del request.session['carrito']
    
    messages.success(request, f'¡Compra finalizada! {len(carrito)} productos procesados.')
    return redirect('rescateComida:perfil_cliente')


