from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Categoría de producto
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Producto único
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre

# Perfil extendido para usuarios del sistema
class PerfilUsuario(models.Model):
    ROLES = [
        ('admin', 'Administrador'),
        ('vendedor', 'Vendedor'),
        ('bodeguero', 'Bodeguero'),
        ('contador', 'Contador'),
        ('cliente', 'Cliente'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')

    def __str__(self):
        return f"{self.user.username} ({self.get_rol_display()})"

# Pedido de productos
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    # Datos para pedidos de invitados
    nombre_cliente = models.CharField(max_length=100, null=True, blank=True)
    correo_cliente = models.EmailField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    comuna = models.CharField(max_length=100, null=True, blank=True)
    calle = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=20, null=True, blank=True)
    complemento = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Pedido #{self.id} - ${self.total}"

# Ítems dentro de un pedido
class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre if self.producto else 'Producto eliminado'}"

@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created and not PerfilUsuario.objects.filter(user=instance).exists():
        PerfilUsuario.objects.create(user=instance, rol='cliente')