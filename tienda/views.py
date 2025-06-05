import requests  # <-- necesario para consumir la API externa
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from tienda.models import Producto, Categoria, Pedido, PedidoItem, PerfilUsuario
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from .forms import UserForm, PerfilUsuarioForm
from tienda.models import PerfilUsuario
from django.http import JsonResponse
import json






def administrador(request):
    usuarios = User.objects.filter(
        perfilusuario__rol__in=['vendedor', 'bodeguero', 'contador', 'administrador']
    )
    productos = Producto.objects.all()
    ventas = Pedido.objects.all()

    context = {
        'usuarios': usuarios,
        'productos': productos,
        'ventas': ventas
    }
    return render(request, 'administrador.html', context)


def vendedor(request):
    return render(request, 'vendedor.html')

def bodeguero(request):
    return render(request, 'bodeguero.html')

def contador(request):
    return render(request, 'contador.html')

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
         } )
def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito

    return redirect('ver_carrito')

from django.shortcuts import render, redirect
from django.contrib import messages
import requests

def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        print("📩 Correo ingresado:", correo)
        print("🔑 Contraseña ingresada:", password)

        if not correo or not password:
            return render(request, 'login.html', {'error': 'Debes ingresar correo y contraseña.'})

        try:
            response = requests.post(
                'http://localhost:8001/usuarios/login',
                data={'email': correo, 'password': password}
            )
            print("📡 Código de respuesta:", response.status_code)
            print("🧾 Respuesta:", response.text)

            if response.status_code == 200:
                usuario = response.json()
                request.session['usuario'] = usuario
                messages.success(request, f"Bienvenido, {usuario['nombre']} 👋")

                tipo = usuario.get('tipo', '').lower()
                print("🔐 Tipo detectado:", tipo)

                if tipo in ['cliente', 'normal']:
                    return redirect('/')
                elif tipo == 'vendedor':
                    return redirect('/vendedor/inicio')
                elif tipo == 'bodeguero':
                    return redirect('/bodega/inicio')
                elif tipo == 'contador':
                    return redirect('/contador/inicio')
                elif tipo == 'administrador':
                    return redirect('/admin/inicio')
                else:
                    return render(request, 'login.html', {'error': 'Tipo de usuario no reconocido.'})
            else:
                return render(request, 'login.html', {
                    'error': response.json().get('detail', 'Credenciales incorrectas')
                })

        except Exception as e:
            print("❌ Error en login:", e)
            return render(request, 'login.html', {'error': f'Error de conexión: {str(e)}'})

    return render(request, 'login.html')



def logout_view(request):
    request.session.flush()
    return redirect('home')

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
            # Consumir producto desde la API externa
            response = requests.get(f"http://localhost:3000/productos/{codigo_producto}")
            if response.status_code == 200:
                datos = response.json()

                # Convertir precio a número
                precio_str = str(datos['precio']).replace('$', '').replace(',', '').strip()
                precio = float(precio_str)

                # Crear estructura de producto
                producto = {
                    'codigo': codigo_producto,
                    'nombre': datos['nombre'],
                    'precio': precio,
                    'imagen': f"/static/img/productos/{datos['imagen']}"  # ruta local correcta
                }

                # Agregar al listado
                subtotal = precio * cantidad
                productos.append({
                    'producto': producto,
                    'cantidad': cantidad,
                    'subtotal': subtotal
                })
                total += subtotal
            else:
                print(f"Producto no encontrado: {codigo_producto}")
        except Exception as e:
            print(f"Error al cargar producto {codigo_producto} →", e)

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

import requests
from django.views.decorators.csrf import csrf_exempt

# Mostrar todos los usuarios (excepto clientes)
def lista_usuarios(request):
    try:
        response = requests.get("http://localhost:8001/usuarios/")
        if response.status_code == 200:
            usuarios = [u for u in response.json() if u['tipo'] != 'cliente']
        else:
            usuarios = []
    except Exception as e:
        print("Error al obtener usuarios:", e)
        usuarios = []

    return render(request, 'administrador.html', {'usuarios': usuarios})


# Crear usuario
@csrf_exempt
def crear_usuario(request):
    if request.method == 'POST':
        data = {
            'rut': request.POST.get('rut'),
            'nombre': request.POST.get('nombre'),
            'email': request.POST.get('email'),
            'pass_': request.POST.get('password'),
            'tipo': request.POST.get('tipo')
        }
        try:
            response = requests.post("http://localhost:8001/usuarios/", data=data)
            if response.status_code in [200, 201]:
                return redirect('/administrador/')
        except Exception as e:
            print("Error al crear usuario:", e)
    return redirect('/administrador/')

# Eliminar usuario
def eliminar_usuario(request, rut):
    try:
        response = requests.delete(f"http://localhost:8001/usuarios/{rut}")
    except Exception as e:
        print("Error al eliminar usuario:", e)
    return redirect('/administrador/')

def admin_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'administrador.html', {'usuarios': usuarios})

def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'form_usuario.html', {'form': form})

def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('admin_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'form_usuario.html', {'form': form})

def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    return redirect('admin_usuarios')

def crear_usuario(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        perfil_form = PerfilUsuarioForm(request.POST)

        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])  # Encriptar contraseña
            user.save()

            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()

            messages.success(request, 'Usuario creado correctamente.')
            return redirect('administrador.html')
    else:
        user_form = UserForm()
        perfil_form = PerfilUsuarioForm()

    return render(request, 'form_usuario.html', {
        'user_form': user_form,
        'perfil_form': perfil_form
    })


@csrf_exempt
def registrar_pedido_paypal(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            usuario = request.user if request.user.is_authenticated else None

            pedido = Pedido.objects.create(
                usuario=usuario,
                total=data['total'],
                nombre_cliente=data['nombre'],
                correo_cliente=data['correo'],
                telefono=data['telefono'],
                region=data['region'],
                comuna=data['comuna'],
                calle=data['calle'],
                numero=data['numero'],
                complemento=data.get('complemento', '')
            )

            if not request.user.is_authenticated:
                request.session['pedido_id'] = pedido.id  # 🔥 Este es el paso importante

            for item in data['productos']:
                producto = Producto.objects.get(id=item['producto_id'])
                PedidoItem.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=item['cantidad'],
                    subtotal=item['subtotal']
                )

            return JsonResponse({'status': 'ok', 'pedido_id': pedido.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)}, status=500)

    return JsonResponse({'status': 'invalid method'}, status=400)


def confirmacion_pago(request):
    if request.user.is_authenticated:
        pedido = Pedido.objects.filter(usuario=request.user).order_by('-fecha').first()
    else:
        pedido_id = request.session.get('pedido_id')
        pedido = Pedido.objects.filter(id=pedido_id).first()

    if not pedido:
        return render(request, 'exito.html', {'nombre': 'Desconocido', 'correo': 'No disponible', 'productos': [], 'total': 0})

    productos = []
    for item in pedido.items.all():
        productos.append({
            'nombre': item.producto.nombre if item.producto else 'Producto eliminado',
            'cantidad': item.cantidad,
            'precio': item.producto.precio if item.producto else 0,
            'subtotal': item.subtotal
        })

    context = {
        'nombre': pedido.nombre_cliente or pedido.usuario.get_full_name() if pedido.usuario else 'Invitado',
        'correo': pedido.correo_cliente or pedido.usuario.email if pedido.usuario else 'No disponible',
        'productos': productos,
        'total': pedido.total
    }

    return render(request, 'exito.html', context)

def home_view(request):
    # Obtener productos desde la API externa
    response = requests.get("http://localhost:8000/api/productos/")
    productos = response.json()

    # Obtener el valor del dólar (ejemplo)
    valor_dolar = 900  # Ojalá obtenido desde una API real

    # Agregar precio en dólares a cada producto
    for producto in productos:
        producto["precio_usd"] = round(float(producto["precio"]) / valor_dolar, 2)


    context = {
        "productos": productos,
        "valor_dolar": valor_dolar
    }
    return render(request, "home.html", context)
