import pytest
import json
from comprar_entradas.models import Usuario, FormaPago, TipoEntrada
from django.core.exceptions import ObjectDoesNotExist

@pytest.mark.django_db
def test_api_realizar_compra_endpoint_retorna_201_y_link_mp(client):
    usuario_real = Usuario.objects.create(nombre="Alexis", apellido="Felippa", email="alexis@test.com")
    FormaPago.objects.create(nombre="TARJETA")
    TipoEntrada.objects.create(nombre="VIP")
    
    payload = {
        "usuario": {"id": usuario_real.id, "nombre": usuario_real.nombre},
        "fecha": "2026-06-16",
        "forma_pago": "TARJETA",
        "entradas": [
            {"edad": 25, "tipo_pase": "VIP", "precio_unitario": 20000.0}
        ]
    }
    
    response = client.post(
        '/api/compras/', 
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    
    data = response.json()
    assert data["mensaje"] == "Compra procesada exitosamente"
    
    assert "mercado_pago_redirect_url" in data
    assert "mercadopago.com.ar" in data["mercado_pago_redirect_url"]

@pytest.mark.django_db
def test_api_realizar_compra_retorna_404_si_usuario_no_existe(client):
   
    FormaPago.objects.create(nombre="TARJETA")
    TipoEntrada.objects.create(nombre="VIP")
    
    payload = {
        "usuario": {"id": 999, "nombre": "Usuario Fantasma"},
        "fecha": "2026-10-10",
        "forma_pago": "TARJETA",
        "entradas": [
            {"edad": 25, "tipo_pase": "VIP"}
        ]
    }
    
    response = client.post(
        '/api/compras/', 
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 404
    
    data = response.json()
    assert data["error"] == "Dato paramétrico no encontrado en la base de datos"

@pytest.mark.django_db
def test_api_realizar_compra_retorna_404_si_tipo_entrada_no_existe(client):
    usuario_real = Usuario.objects.create(nombre="Prueba", apellido="Test", email="prueba@test.com")
    FormaPago.objects.create(nombre="TARJETA")
    
    payload = {
        "usuario": {"id": usuario_real.id, "nombre": usuario_real.nombre},
        "fecha": "2026-10-10",
        "forma_pago": "TARJETA",
        "entradas": [
            {"edad": 25, "tipo_pase": "INVENTADO"} 
        ]
    }
    
    response = client.post(
        '/api/compras/', 
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 404
    
    data = response.json()
    assert data["error"] == "Dato paramétrico no encontrado en la base de datos"