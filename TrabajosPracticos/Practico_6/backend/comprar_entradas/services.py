from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from .models import Compra, Entrada, Usuario, FormaPago, TipoEntrada
from .validators import (
    validar_usuario_registrado, validar_cantidad_entradas,
    validar_fecha_visita, validar_forma_pago
)

MERCADO_PAGO_BASE_URL = "https://www.mercadopago.com.ar/checkout/v1/redirect"

def procesar_compra(datos):
    # 1. Validaciones de negocio puras
    validar_usuario_registrado(datos.get("usuario"))
    validar_cantidad_entradas(datos.get("entradas"))
    validar_fecha_visita(datos.get("fecha"))
    validar_forma_pago(datos.get("forma_pago"))
    
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

    # Enviar email de confirmación
    email_destino = datos.get("email_confirmacion") or usuario.email
    entradas_data = datos.get("entradas", [])
    detalle = "\n".join(
        f"  - Entrada {i+1}: {item['tipo_pase']} | Edad: {item['edad']} años | ${item['precio_unitario']:,.0f}"
        for i, item in enumerate(entradas_data)
    )
    forma_pago_texto = "Tarjeta de crédito (Mercado Pago)" if datos["forma_pago"] == "TARJETA" else "Efectivo en boletería"
    mp_linea = ""
    if nueva_compra.mercado_pago_redirect_url:
        mp_linea = f"\nCompletá tu pago en Mercado Pago:\n{nueva_compra.mercado_pago_redirect_url}\n"
    cuerpo = (
        f"Hola {usuario.nombre} {usuario.apellido},\n\n"
        f"¡Tu compra en EcoHarmony Park fue confirmada!\n\n"
        f"  N.° de compra:    #{nueva_compra.id}\n"
        f"  Fecha de visita:  {nueva_compra.fecha.strftime('%d/%m/%Y')}\n"
        f"  Cantidad entradas: {nueva_compra.cantidad_entradas}\n"
        f"  Forma de pago:    {forma_pago_texto}\n\n"
        f"Detalle de entradas:\n{detalle}\n\n"
        f"  TOTAL:  ${nueva_compra.monto_total:,.0f}\n"
        f"{mp_linea}\n"
        f"¡Te esperamos en EcoHarmony Park!\n"
        f"El equipo de EcoHarmony Park"
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