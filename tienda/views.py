from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.http import require_POST

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

