# tienda/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
     path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('registro/', views.registro_view, name='registro'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('confirmar/', views.confirmar_compra, name='confirmar_compra'),
    path('contacto/', views.contacto_view, name='contacto'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),





]

