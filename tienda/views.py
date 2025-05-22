from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Vista principal que muestra todos los productos
def home(request):
    productos = Producto.objects.all()
    return render(request, 'home.html', {'productos': productos})

# Vista de detalle de un producto específico
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'detalle.html', {'producto': producto})

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        carrito[str(producto_id)] += 1
    else:
        carrito[str(producto_id)] = 1

    request.session['carrito'] = carrito
    return redirect('ver_carrito')


def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0

    for id_str, cantidad in carrito.items():
        producto = Producto.objects.get(id=int(id_str))
        subtotal = producto.precio * cantidad
        total += subtotal
        productos.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal
        })

    return render(request, 'carrito.html', {'productos': productos, 'total': total})


def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito

    return redirect('ver_carrito')

def registro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'registro.html', {'error': 'Ese nombre de usuario ya está en uso.'})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)  # Login automático tras registrarse
        return redirect('/')
    
    return render(request, 'registro.html')

def checkout_view(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0

    for id_str, cantidad in carrito.items():
        producto = Producto.objects.get(id=int(id_str))
        subtotal = producto.precio * cantidad
        total += subtotal
        productos.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal
        })

    return render(request, 'checkout.html', {'productos': productos, 'total': total})


@require_POST
def confirmar_compra(request):
    # Aquí podrías guardar la orden en una base de datos real
    request.session['carrito'] = {}
    return render(request, 'exito.html')

def contacto_view(request):
    return render(request, 'contacto.html')

def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, 'productos_por_categoria.html', {
        'categoria': categoria,
        'productos': productos
    })

@require_http_methods(["GET", "POST"])
def checkout_invitado(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        direccion = request.POST.get('direccion')

        # Validación básica
        if not nombre or not correo or not direccion:
            return render(request, 'checkout_invitado.html', {
                'error': 'Todos los campos son obligatorios.',
                'nombre': nombre,
                'correo': correo,
                'direccion': direccion
            })

        try:
            validate_email(correo)
        except ValidationError:
            return render(request, 'checkout_invitado.html', {
                'error': 'Correo inválido.',
                'nombre': nombre,
                'correo': correo,
                'direccion': direccion
            })

        # Crear pedido como invitado
        carrito = request.session.get('carrito', {})
        if not carrito:
            return redirect('/')

        total = 0
        pedido = Pedido.objects.create(
            usuario=None,
            total=0,
            nombre_cliente=nombre,
            correo_cliente=correo,
            direccion_cliente=direccion
        )

        for id_str, cantidad in carrito.items():
            producto = Producto.objects.get(id=int(id_str))
            subtotal = producto.precio * cantidad
            PedidoItem.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                subtotal=subtotal
            )
            total += subtotal

        pedido.total = total
        pedido.save()
        request.session['carrito'] = {}

        return redirect('pago_pendiente', pedido_id=pedido.id)

    return render(request, 'checkout_invitado.html')