import requests  # <-- necesario para consumir la API externa

from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria, Pedido, PedidoItem
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
<<<<<<< HEAD

=======
from django.contrib import messages
>>>>>>> 9c50cf0 (actualizacion de uso de apis para iniciar sesion)

def home(request):
    try:
        respuesta = requests.get("http://localhost:3000/productos")  # Asegúrate de que esta URL esté activa
        if respuesta.status_code == 200:
            productos = respuesta.json()
        else:
            productos = []
    except Exception as e:
        print("Error al consumir API de productos:", e)
        productos = []

    return render(request, 'home.html', {'productos': productos})

# Vista de detalle de un producto específico
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'detalle.html', {'producto': producto})

# def agregar_al_carrito(request, producto_id):
#     producto = get_object_or_404(Producto, id=producto_id)
#     carrito = request.session.get('carrito', {})

#     if str(producto_id) in carrito:
#         carrito[str(producto_id)] += 1
#     else:
#         carrito[str(producto_id)] = 1

#     request.session['carrito'] = carrito
#     return redirect('ver_carrito')

def agregar_al_carrito_api(request, codigo_producto):
    if request.method == 'POST':
        try:
            url = f"http://localhost:3000/productos/{codigo_producto}"
            response = requests.get(url)

            if response.status_code == 200:
                carrito = request.session.get('carrito', {})

                if codigo_producto in carrito:
                    carrito[codigo_producto] += 1
                else:
                    carrito[codigo_producto] = 1

                request.session['carrito'] = carrito
        except Exception as e:
            print("Error al agregar producto desde API:", e)

    return redirect('home')


def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0

    for codigo_producto, cantidad in carrito.items():
        try:
            # Consultar producto desde la API
            response = requests.get(f"http://localhost:3000/productos/{codigo_producto}")
            if response.status_code == 200:
                datos = response.json()

                # Limpieza del precio para convertirlo a float
                precio_str = str(datos['precio']).replace('$', '').replace(',', '').strip()
                precio = float(precio_str)

                producto = {
                    'codigo': codigo_producto,
                    'nombre': datos['nombre'],
                    'precio': precio,
                    'imagen': datos.get('imagen', '')
                }

                subtotal = precio * cantidad
                productos.append({
                    'producto': producto,
                    'cantidad': cantidad,
                    'subtotal': subtotal
                })

                total += subtotal
            else:
                print(f"Producto no encontrado en API: {codigo_producto}")

        except Exception as e:
            print(f"Error cargando producto desde API: {codigo_producto} →", e)

    return render(request, 'carrito.html', {
        'productos': productos,
        'total': total
    })

<<<<<<< HEAD



=======
>>>>>>> 9c50cf0 (actualizacion de uso de apis para iniciar sesion)
def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito

    return redirect('ver_carrito')

<<<<<<< HEAD
=======

def login_view(request):
    if request.method == 'POST':
        rut = request.POST.get('username')
        password = request.POST.get('password')

        if not rut or not password:
            return render(request, 'login.html', {'error': 'Debes ingresar RUT y contraseña.'})

        try:
            response = requests.post(
                'http://localhost:8001/usuarios/login',
                data={'rut': rut, 'password': password}
            )

            if response.status_code == 200:
                usuario = response.json()
                request.session['usuario'] = usuario
                messages.success(request, f"Bienvenido, {usuario['nombre']} 👋")
                return redirect('/')
            else:
                return render(request, 'login.html', {
                    'error': response.json().get('detail', 'Credenciales incorrectas')
                })

        except Exception as e:
            return render(request, 'login.html', {'error': f'Error de conexión: {str(e)}'})

    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('home')


>>>>>>> 9c50cf0 (actualizacion de uso de apis para iniciar sesion)
def registro_view(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('pass')  # debe coincidir con 'pass_' en la API
        tipo = request.POST.get('tipo', 'normal')

        if not all([rut, nombre, email, password]):
            return render(request, 'registro.html', {
                'error': 'Todos los campos son obligatorios.'
            })

        try:
            # Usa data= para enviar como formulario (form-urlencoded)
            response = requests.post('http://localhost:8001/usuarios/', data={
                'rut': rut,
                'nombre': nombre,
                'email': email,
                'pass_': password,  # usa pass_ porque la API lo espera así
                'tipo': tipo
            })

            if response.status_code in [200, 201]:
                return redirect('/login/')
            else:
                return render(request, 'registro.html', {
                    'error': f"Error al registrar usuario: {response.json().get('detail', 'Error desconocido')}"
                })

        except Exception as e:
            return render(request, 'registro.html', {
                'error': f"Error de conexión con la API: {str(e)}"
            })

    return render(request, 'registro.html')

 
def checkout_view(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0

    for codigo_producto, cantidad in carrito.items():
        try:
            response = requests.get(f"http://localhost:3000/productos/{codigo_producto}")
            if response.status_code == 200:
                datos = response.json()

                precio_str = str(datos['precio']).replace('$', '').replace(',', '').strip()
                precio = float(precio_str)

                producto = {
                    'codigo': codigo_producto,
                    'nombre': datos['nombre'],
                    'precio': precio,
                    'imagen': datos.get('imagen', '')
                }

                subtotal = precio * cantidad
                productos.append({
                    'producto': producto,
                    'cantidad': cantidad,
                    'subtotal': subtotal
                })
                total += subtotal
        except Exception as e:
            print(f"Error cargando producto desde API en checkout: {codigo_producto} →", e)

    return render(request, 'checkout.html', {
        'productos': productos,
        'total': total
    })




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
        telefono = request.POST.get('telefono')
        region = request.POST.get('region')
        comuna = request.POST.get('comuna')
        calle = request.POST.get('calle')
        numero = request.POST.get('numero')
        complemento = request.POST.get('complemento')

        # Validación básica
        if not all([nombre, correo, telefono, region, comuna, calle, numero]):
            return render(request, 'checkout_invitado.html', {
                'error': 'Todos los campos obligatorios deben estar completos.',
                'nombre': nombre, 'correo': correo, 'telefono': telefono,
                'region': region, 'comuna': comuna, 'calle': calle,
                'numero': numero, 'complemento': complemento
            })

        try:
            validate_email(correo)
        except ValidationError:
            return render(request, 'checkout_invitado.html', {
                'error': 'Correo electrónico inválido.',
                'nombre': nombre, 'correo': correo, 'telefono': telefono,
                'region': region, 'comuna': comuna, 'calle': calle,
                'numero': numero, 'complemento': complemento
            })

        # Verificamos que haya algo en el carrito
        carrito = request.session.get('carrito', {})
        if not carrito:
            return redirect('/')

        productos = []
        total = 0

        for codigo_producto, cantidad in carrito.items():
            try:
                response = requests.get(f"http://localhost:3000/productos/{codigo_producto}")
                if response.status_code == 200:
                    datos = response.json()
                    precio = float(str(datos['precio']).replace('$', '').replace(',', '').strip())
                    subtotal = precio * cantidad
                    producto = {
                        'codigo': codigo_producto,
                        'nombre': datos['nombre'],
                        'precio': precio,
                        'imagen': datos.get('imagen', ''),
                        'cantidad': cantidad,
                        'subtotal': subtotal
                    }
                    productos.append(producto)
                    total += subtotal
            except Exception as e:
                print(f"Error cargando producto desde API en checkout_invitado: {codigo_producto} →", e)

        # Aquí podrías guardar los datos del pedido en la base si lo deseas
        request.session['carrito'] = {}

        # Simulamos confirmación del pedido con ID ficticio
        return render(request, 'exito.html', {
            'nombre': nombre,
            'correo': correo,
            'productos': productos,
            'total': total
        })

    return render(request, 'checkout_invitado.html')


def productos_externos(request):
    try:
        respuesta = requests.get("http://localhost:3000/productos")  # Asegúrate de que tu API esté corriendo
        if respuesta.status_code == 200:
            productos = respuesta.json()
        else:
            productos = []
    except Exception as e:
        print("Error al consumir API:", e)
        productos = []

    return render(request, 'productos_externos.html', {'productos': productos})

def agregar_al_carrito_api(request, codigo_producto):
    if request.method == 'POST':
        try:
            # Llamar a tu API Express por el código de producto
            url = f"http://localhost:3000/productos/{codigo_producto}"
            response = requests.get(url)

            if response.status_code == 200:
                producto = response.json()

                # Acceder a la sesión del carrito
                carrito = request.session.get('carrito', {})

                # Sumar cantidad o agregar nuevo
                if codigo_producto in carrito:
                    carrito[codigo_producto] += 1
                else:
                    carrito[codigo_producto] = 1

                request.session['carrito'] = carrito
        except Exception as e:
            print("Error al agregar producto desde API:", e)

    return redirect('home')  # Redirigir al home u otra vista