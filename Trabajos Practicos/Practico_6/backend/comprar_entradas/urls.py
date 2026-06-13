from django.urls import path
from . import views

urlpatterns = [
    path('api/compras/', views.api_realizar_compra, name='api_compras'),
    path('api/usuarios/', views.api_usuarios, name='api_usuarios'),
    path('api/mis-compras/', views.api_mis_compras, name='api_mis_compras'),
]