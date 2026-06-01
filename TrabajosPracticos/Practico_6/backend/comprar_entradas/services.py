from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from .models import Compra, Entrada, Usuario, FormaPago, TipoEntrada
from .validators import (
    validar_usuario_registrado, validar_cantidad_entradas,
    validar_fecha_visita, validar_forma_pago,
    validar_tipo_pase, validar_datos_visitantes
)

MERCADO_PAGO_BASE_URL = "https://www.mercadopago.com.ar/checkout/v1/redirect"

PRECIO_VIP = 20000.0
PRECIO_REGULAR = 10000.0

def calcular_precio(edad, tipo_pase):
    """Calcula el precio según tipo de pase y edad del visitante."""
    base = PRECIO_VIP if tipo_pase == "VIP" else PRECIO_REGULAR
    if edad <= 3:
        return 0.0
    if edad <= 15 or edad >= 60:
        return base * 0.5
    return base

def procesar_compra(datos):
    
    validar_usuario_registrado(datos.get("usuario"))
    validar_cantidad_entradas(datos.get("entradas"))
    validar_fecha_visita(datos.get("fecha"))
    validar_forma_pago(datos.get("forma_pago"))
    for entrada in datos.get("entradas", []):
        validar_tipo_pase(entrada.get("tipo_pase", ""))
    validar_datos_visitantes(datos.get("entradas", []))

    # 2. Buscar entidades en la BD
    usuario = Usuario.objects.get(id=datos["usuario"]["id"])
    forma_pago = FormaPago.objects.get(nombre=datos["forma_pago"])

    entradas_data = datos.get("entradas", [])
    cantidad = len(entradas_data)
    # Calcular precios server-side según edad y tipo de pase
    precios = [calcular_precio(item["edad"], item["tipo_pase"]) for item in entradas_data]
    monto_total = sum(precios)

    # 3. Guardar en BD

    with transaction.atomic():
        nueva_compra = Compra.objects.create(
            usuario=usuario,
            fecha=datos["fecha"],
            cantidad_entradas=cantidad,
            monto_total=monto_total,
            forma_pago=forma_pago,
            mercado_pago_redirect_url=None
        )
        
        for item, precio in zip(entradas_data, precios):
            tipo_entrada = TipoEntrada.objects.get(nombre=item["tipo_pase"])
            Entrada.objects.create(
                compra=nueva_compra,
                edad=item["edad"],
                tipo_entrada=tipo_entrada,
                precio_unitario=precio
            )

        # Generar URL de Mercado Pago si el pago es con tarjeta
        if datos["forma_pago"] == "TARJETA":
            nueva_compra.mercado_pago_redirect_url = (
                f"{MERCADO_PAGO_BASE_URL}?pref_id=COMPRA-{nueva_compra.id}"
            )
            nueva_compra.save()

    # Enviar mail de confirmación en segundo plano (no bloquea la respuesta HTTP)
    email_destino = datos.get("email_confirmacion") or usuario.email

    detalle_entradas = "\n".join(
        f"  - Entrada {i+1}: {item['tipo_pase']} | Edad: {item['edad']} años | ${precio:,.0f}"
        for i, (item, precio) in enumerate(zip(entradas_data, precios))
    )

    forma_pago_texto = "Tarjeta de crédito (Mercado Pago)" if datos["forma_pago"] == "TARJETA" else "Efectivo en boletería"

    mp_linea = ""
    if nueva_compra.mercado_pago_redirect_url:
        mp_linea = f"\nCompletá tu pago en Mercado Pago:\n{nueva_compra.mercado_pago_redirect_url}\n"

    cuerpo = (
        f"Hola {usuario.nombre} {usuario.apellido},\n\n"
        f"¡Tu compra en EcoHarmony Park fue confirmada!\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"  N.° de compra:    #{nueva_compra.id}\n"
        f"  Fecha de visita:  {nueva_compra.fecha.strftime('%d/%m/%Y')}\n"
        f"  Cantidad entradas: {nueva_compra.cantidad_entradas}\n"
        f"  Forma de pago:    {forma_pago_texto}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Detalle de entradas:\n{detalle_entradas}\n\n"
        f"  TOTAL:  ${nueva_compra.monto_total:,.0f}\n"
        f"{mp_linea}\n"
        f"¡Te esperamos en EcoHarmony Park!\n"
        f"El equipo de EcoHarmony Park\n"
        f"info@ecoharmonypark.com"
    )

    try:
        send_mail(
            subject=f"Confirmación de compra #{nueva_compra.id} - EcoHarmony Park",
            message=cuerpo,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email_destino],
            fail_silently=False,
        )
    except Exception as e:
        print(f"[EMAIL ERROR] No se pudo enviar a {email_destino}: {e}")

    return nueva_compra