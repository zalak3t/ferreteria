# tienda/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('productos/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('registro/', views.registro_view, name='registro'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('confirmar/', views.confirmar_compra, name='confirmar_compra'),
    path('contacto/', views.contacto_view, name='contacto'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('checkout/invitado/', views.checkout_invitado, name='checkout_invitado'),
    path('productos-api/', views.productos_externos, name='productos_api'),
    path('agregar-api/<str:codigo_producto>/', views.agregar_al_carrito_api, name='agregar_al_carrito_api'),
    path('eliminar-carrito/<str:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('admin/inicio', views.administrador, name='admin_inicio'),
    path('vendedor/inicio', views.vendedor, name='vendedor_inicio'),
    path('bodega/inicio', views.bodeguero, name='bodeguero_inicio'),
    path('contador/inicio', views.contador, name='contador_inicio'),
    path('administrador/', views.lista_usuarios, name='administrador'),
    path('administrador/crear/', views.crear_usuario, name='crear_usuario'),
    path('administrador/eliminar/<str:rut>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('admin/usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('admin/usuarios/nuevo/', views.crear_usuario, name='crear_usuario'),
    path('admin/usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('admin/usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('administrador/', views.administrador, name='panel_admin'),
     path('api/registrar_pedido_paypal/', views.registrar_pedido_paypal, name='registrar_pedido_paypal'),
     path('confirmacion_pago/', views.confirmacion_pago, name='confirmacion_pago'),










   ]




