from django.db import transaction
from django.core.mail import send_mail
from .models import Compra, Entrada, Usuario, FormaPago, TipoEntrada
from .validators import (
    validar_usuario_registrado, validar_cantidad_entradas,
    validar_fecha_visita, validar_forma_pago,
    validar_tipo_pase, validar_datos_visitantes
)

MERCADO_PAGO_BASE_URL = "https://www.mercadopago.com.ar/checkout/v1/redirect"

def procesar_compra(datos):
    # 1. Validaciones de negocio puras
    validar_usuario_registrado(datos.get("usuario"))
    validar_cantidad_entradas(datos.get("entradas"))
    validar_fecha_visita(datos.get("fecha"))
    validar_forma_pago(datos.get("forma_pago"))
    for entrada in datos.get("entradas", []):
        validar_tipo_pase(entrada.get("tipo_pase", ""))
    validar_datos_visitantes(datos.get("entradas", []))
    
    # 2. Buscar las entidades reales en la BD
    usuario = Usuario.objects.get(id=datos["usuario"]["id"])
    forma_pago = FormaPago.objects.get(nombre=datos["forma_pago"])
    
    entradas_data = datos.get("entradas", [])
    cantidad = len(entradas_data)
    
    # Calculamos el monto total sumando los precios unitarios
    monto_total = sum(item["precio_unitario"] for item in entradas_data)
    
    # 3. Transacción atómica para guardar todo junto
    with transaction.atomic():
        nueva_compra = Compra.objects.create(
            usuario=usuario,
            fecha=datos["fecha"],
            cantidad_entradas=cantidad,
            monto_total=monto_total,
            forma_pago=forma_pago,
            mercado_pago_redirect_url=None
        )
        
        for item in entradas_data:
            tipo_entrada = TipoEntrada.objects.get(nombre=item["tipo_pase"])
            Entrada.objects.create(
                compra=nueva_compra,
                edad=item["edad"],
                tipo_entrada=tipo_entrada,
                precio_unitario=item["precio_unitario"]
            )

        # Generar URL de Mercado Pago si el pago es con tarjeta
        if datos["forma_pago"] == "TARJETA":
            nueva_compra.mercado_pago_redirect_url = (
                f"{MERCADO_PAGO_BASE_URL}?pref_id=COMPRA-{nueva_compra.id}"
            )
            nueva_compra.save()

    # Enviar mail de confirmación
    send_mail(
        subject="Confirmación de compra - EcoHarmony Park",
        message=(
            f"Hola {usuario.nombre},\n\n"
            f"Tu compra fue confirmada.\n"
            f"Entradas: {nueva_compra.cantidad_entradas}\n"
            f"Fecha de visita: {nueva_compra.fecha}\n"
            f"Total: ${nueva_compra.monto_total}\n\n"
            f"¡Te esperamos en EcoHarmony Park!"
        ),
        from_email="noreply@ecoharmonypark.com",
        recipient_list=[usuario.email],
        fail_silently=True,
    )

    return nueva_compra