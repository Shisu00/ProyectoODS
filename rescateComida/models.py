from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('cliente', 'Cliente'),
        ('proveedor', 'Proveedor'),
        ('organizacion', 'Organizacion'),
        ('admin', 'Administrador'),
    ]
  
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='cliente'
    )
    telefono = models.CharField(max_length=12, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    comuna = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def nombre(self):
        return self.first_name or self.username

    @property
    def correo(self):
        return self.email



class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'categoria'

    def __str__(self):
        return self.nombre_categoria



class Producto(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('no_disponible', 'No disponible'),
        ('reservado', 'Reservado'),
    ]

    UNIDADES = [
        ('kg', 'Kilogramos'),
        ('g', 'Gramos'),
        ('lt', 'Litros'),
        ('ml', 'Mililitros'),
        ('unidad', 'Unidad'),
        ('caja', 'Caja'),
    ]

    id_producto = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='productos'
    )
    id_categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        db_column='id_categoria',
        blank=True,
        null=True
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    cantidad = models.IntegerField()
    unidad_medida = models.CharField(
        max_length=20,
        choices=UNIDADES,
        default='unidad'
    )
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    estado = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='disponible'
    )
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    class Meta:
        db_table = 'producto'

    def __str__(self):
        return self.nombre



class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('venta', 'Venta'),
        ('donacion', 'Donacion'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

    id_transaccion = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        db_column='id_producto',
        related_name='transacciones'
    )
    id_cliente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_cliente',
        related_name='transacciones_cliente'
    )
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    tipo = models.CharField(
        max_length=8,
        choices=TIPO_CHOICES
    )
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )

    class Meta:
        db_table = 'transaccion'

    def __str__(self):
        return f"Transaccion #{self.id_transaccion}"



class Valoracion(models.Model):
    id_valoracion = models.AutoField(primary_key=True)
    id_transaccion = models.ForeignKey(
        Transaccion,
        on_delete=models.CASCADE,
        db_column='id_transaccion',
        related_name='valoraciones'
    )
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='valoraciones'
    )
    puntuacion = models.IntegerField()
    comentario = models.TextField(blank=True, null=True)
    fecha_valoracion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'valoracion'

    def __str__(self):
        return f"Valoracion de {self.id_usuario} - {self.puntuacion}/5"
