# comprar_entradas/services.py
from django.db import transaction
from .models import Compra, Entrada
from .validators import (
    validar_usuario_registrado, validar_cantidad_entradas,
    validar_fecha_visita, validar_forma_pago
)

def procesar_compra(datos):
    
    validar_usuario_registrado(datos.get("usuario"))
    validar_cantidad_entradas(datos.get("entradas"))
    validar_fecha_visita(datos.get("fecha"))
    validar_forma_pago(datos.get("forma_pago"))
    
    # 2. Transacción atómica: blindamos la base de datos
    with transaction.atomic():
        nueva_compra = Compra.objects.create(
            usuario_id=datos["usuario"]["id"],
            fecha_visita=datos["fecha"],
            forma_pago=datos["forma_pago"]
        )
        
        for entrada_data in datos.get("entradas", []):
            Entrada.objects.create(
                compra=nueva_compra,
                edad=entrada_data["edad"],
                tipo_pase=entrada_data["tipo_pase"]
            )
            
    return nueva_compra