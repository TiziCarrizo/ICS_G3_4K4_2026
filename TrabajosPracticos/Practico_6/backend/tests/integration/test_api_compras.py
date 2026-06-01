import pytest
import json
from comprar_entradas.models import Usuario, FormaPago, TipoEntrada

@pytest.mark.django_db
def test_api_realizar_compra_endpoint_retorna_201(client):
    # Arrange: Preparamos la base de datos
    usuario_real = Usuario.objects.create(nombre="Alexis", apellido="G", email="alexis@test.com")
    FormaPago.objects.create(nombre="TARJETA")
    TipoEntrada.objects.create(nombre="VIP")
    
    # Este es el JSON exacto que te va a mandar tu código de frontend
    payload = {
        "usuario": {"id": usuario_real.id, "nombre": usuario_real.nombre},
        "fecha": "2026-06-15",
        "forma_pago": "TARJETA",
        "entradas": [
            {"edad": 25, "tipo_pase": "VIP", "precio_unitario": 5000.0}
        ]
    }
    
    # Act: Simulamos un POST request desde el cliente (React/HTML) hacia nuestra futura ruta
    response = client.post(
        '/api/compras/', 
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    # Assert: Esperamos un 201 (Created) y un mensaje de éxito
    assert response.status_code == 201
    assert response.json()["mensaje"] == "Compra procesada exitosamente"