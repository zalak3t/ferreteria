# tienda/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
<<<<<<< HEAD
=======
from .views import logout_view

>>>>>>> 9c50cf0 (actualizacion de uso de apis para iniciar sesion)

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
     path('carrito/', views.ver_carrito, name='ver_carrito'),
   # path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('registro/', views.registro_view, name='registro'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('confirmar/', views.confirmar_compra, name='confirmar_compra'),
    path('contacto/', views.contacto_view, name='contacto'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('checkout/invitado/', views.checkout_invitado, name='checkout_invitado'),
    path('productos-api/', views.productos_externos, name='productos_api'),
    path('agregar-api/<str:codigo_producto>/', views.agregar_al_carrito_api, name='agregar_al_carrito_api'),
    path('eliminar-carrito/<str:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
<<<<<<< HEAD
=======
    path('logout/', logout_view, name="logout"),


>>>>>>> 9c50cf0 (actualizacion de uso de apis para iniciar sesion)
   






]

