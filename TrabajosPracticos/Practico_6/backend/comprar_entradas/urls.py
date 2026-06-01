from django.urls import path
from .views import ComprarEntradaView, UsuariosView, MisComprasView

urlpatterns = [
    path('comprar/', ComprarEntradaView.as_view(), name='comprar-entrada'),
    path('usuarios/', UsuariosView.as_view(), name='usuarios'),
    path('mis-compras/', MisComprasView.as_view(), name='mis-compras'),
]
