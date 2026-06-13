import threading
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from .models import Compra, Entrada, Usuario, FormaPago, TipoEntrada
from .validators import (
    validar_usuario_registrado, validar_cantidad_entradas,
    validar_fecha_visita, validar_forma_pago, validar_edades_visitantes
)

MERCADO_PAGO_BASE_URL = "https://www.mercadopago.com.ar/checkout/v1/redirect"

# --- NUEVA FUNCIÓN PARA EL HILO SECUNDARIO ---
def enviar_correo_en_segundo_plano(asunto, mensaje, origen, destinatarios):
    try:
        send_mail(
            subject=asunto,
            message=mensaje,
            from_email=origen,
            recipient_list=destinatarios,
            fail_silently=False,
        )
    except Exception as e:
        print(f"[EMAIL ERROR] No se pudo enviar a {destinatarios}: {e}")
# ---------------------------------------------

def calcular_precio_real(tipo_pase_nombre, edad):
    base = 20000.0 if tipo_pase_nombre == "VIP" else 10000.0
    if edad <= 3: return 0.0
    if edad <= 15 or edad >= 60: return base * 0.5
    return base

def procesar_compra(datos):
    # 1. Validaciones de negocio puras
    validar_usuario_registrado(datos.get("usuario"))
    validar_cantidad_entradas(datos.get("entradas"))
    validar_fecha_visita(datos.get("fecha"))
    validar_forma_pago(datos.get("forma_pago"))
    validar_edades_visitantes(datos.get("entradas"))
    
    # 2. Buscar entidades
    usuario = Usuario.objects.get(id=datos["usuario"]["id"])
    forma_pago = FormaPago.objects.get(nombre=datos["forma_pago"])
    entradas_data = datos.get("entradas", [])
    
    # 3. Transacción atómica
    with transaction.atomic():
        monto_total = sum(calcular_precio_real(item["tipo_pase"], item["edad"]) for item in entradas_data)
        
        nueva_compra = Compra.objects.create(
            usuario=usuario,
            fecha=datos["fecha"],
            cantidad_entradas=len(entradas_data),
            monto_total=monto_total,
            forma_pago=forma_pago,
            mercado_pago_redirect_url=None
        )
        
        if datos["forma_pago"] == "TARJETA":
            nueva_compra.mercado_pago_redirect_url = f"{MERCADO_PAGO_BASE_URL}?pref_id=COMPRA-{nueva_compra.id}"
            nueva_compra.save()
        
        for item in entradas_data:
            tipo_entrada = TipoEntrada.objects.get(nombre=item["tipo_pase"])
            precio_real = calcular_precio_real(item["tipo_pase"], item["edad"])
            Entrada.objects.create(
                compra=nueva_compra,
                edad=item["edad"],
                tipo_entrada=tipo_entrada,
                precio_unitario=precio_real
            )

    # 4. Envío de email (AHORA EN SEGUNDO PLANO)
    email_destino = datos.get("email_confirmacion") or usuario.email
    detalle = "\n".join(
        f"  - Entrada {i+1}: {item['tipo_pase']} | Edad: {item['edad']} años | ${calcular_precio_real(item['tipo_pase'], item['edad']):,.0f}"
        for i, item in enumerate(entradas_data)
    )
    forma_pago_texto = "Tarjeta de crédito (Mercado Pago)" if datos["forma_pago"] == "TARJETA" else "Efectivo en boletería"
    mp_linea = f"\nCompletá tu pago en Mercado Pago:\n{nueva_compra.mercado_pago_redirect_url}\n" if nueva_compra.mercado_pago_redirect_url else ""
    
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
    
    # Creamos el hilo y lo arrancamos para que el mail se mande "por detrás"
    hilo_mail = threading.Thread(
        target=enviar_correo_en_segundo_plano,
        args=(
            f"Confirmación de compra #{nueva_compra.id} - EcoHarmony Park", # Asunto
            cuerpo, # Mensaje
            settings.EMAIL_HOST_USER, # Origen
            [email_destino] # Destinatarios
        )
    )
    hilo_mail.start()

    return nueva_compra