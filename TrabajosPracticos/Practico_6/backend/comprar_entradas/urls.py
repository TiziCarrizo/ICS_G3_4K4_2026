from django.urls import path
from . import views

urlpatterns = [
    path('api/compras/', views.api_realizar_compra, name='api_compras'),
]