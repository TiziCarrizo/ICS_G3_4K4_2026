import pytest
from datetime import date, timedelta

try:
    from comprar_entradas.services import (
        validar_usuario_registrado, validar_cantidad_entradas,
        validar_fecha_visita, validar_forma_pago, procesar_compra,
        calcular_precio
    )
    from comprar_entradas.validators import validar_tipo_pase, validar_datos_visitantes

    from comprar_entradas.models import Compra, Entrada, Usuario, FormaPago, TipoEntrada
except ImportError:
    import pytest
    pytest.fail("RED: Faltan definir los nuevos modelos normalizados en models.py")

@pytest.fixture
def fecha_futura():
    # Busca el próximo día disponible (no lunes, no feriado) a partir de hoy +1
    FERIADOS = [(12, 25), (1, 1)]
    candidato = date.today() + timedelta(days=1)
    while candidato.weekday() == 0 or (candidato.month, candidato.day) in FERIADOS:
        candidato += timedelta(days=1)
    return candidato


# --- TESTS DE VALIDACIÓN ---

def test_validar_usuario_rechaza_usuario_no_registrado():
    usuario_invalido = {"nombre": "Visitante Anónimo"}
    with pytest.raises(ValueError, match="El usuario no está registrado"):
        validar_usuario_registrado(usuario_invalido)


def test_validar_cantidad_entradas_rechaza_mas_de_10():
    # Creamos una lista con 11 visitantes para forzar el error
    entradas_invalidas = [{"edad": 20, "tipo_pase": "REGULAR"} for _ in range(11)]
    with pytest.raises(ValueError, match="La cantidad de entradas supera el máximo permitido"):
        validar_cantidad_entradas(entradas_invalidas)


def test_validar_fecha_rechaza_fechas_pasadas():
    fecha_pasada = date.today() - timedelta(days=1)
    with pytest.raises(ValueError, match="La fecha de visita no puede ser una fecha pasada"):
        validar_fecha_visita(fecha_pasada)


def test_validar_fecha_rechaza_dias_cerrados(fecha_futura):
    dias_para_lunes = (0 - fecha_futura.weekday()) % 7
    fecha_lunes = fecha_futura + timedelta(days=dias_para_lunes)
    with pytest.raises(ValueError, match="El parque está cerrado los lunes"):
        validar_fecha_visita(fecha_lunes)


def test_validar_fecha_rechaza_navidad():
    # Buscar el próximo 25/12 que no sea lunes
    anio = date.today().year
    navidad = date(anio if date(anio, 12, 25) >= date.today() else anio + 1, 12, 25)
    with pytest.raises(ValueError, match="días festivos"):
        validar_fecha_visita(navidad)


def test_validar_fecha_rechaza_anio_nuevo():
    anio_nuevo = date(date.today().year + 1, 1, 1)
    with pytest.raises(ValueError, match="días festivos"):
        validar_fecha_visita(anio_nuevo)


def test_validar_forma_pago_rechaza_opcion_invalida():
    pago_invalido = "TRANSFERENCIA"
    with pytest.raises(ValueError, match="Forma de pago no válida"):
        validar_forma_pago(pago_invalido)


def test_validar_forma_pago_rechaza_sin_seleccion():
    # Mapea la prueba de usuario: "Probar comprar entradas sin seleccionar forma de pago (falla)"
    for valor_vacio in [None, ""]:
        with pytest.raises(ValueError, match="Forma de pago no válida"):
            validar_forma_pago(valor_vacio)


def test_validar_tipo_pase_rechaza_tipo_invalido():
    with pytest.raises(ValueError, match="Tipo de pase no válido"):
        validar_tipo_pase("PREMIUM")


def test_validar_tipo_pase_acepta_vip_y_regular():
    validar_tipo_pase("VIP")      # no lanza excepción
    validar_tipo_pase("REGULAR")  # no lanza excepción


def test_validar_datos_visitantes_acepta_edad_cero():
    # Edad 0 es válida (bebé, no paga)
    entradas_validas = [{"edad": 0, "tipo_pase": "REGULAR", "precio_unitario": 10000}]
    validar_datos_visitantes(entradas_validas)  # no debe lanzar excepción


def test_validar_datos_visitantes_rechaza_sin_campo_edad():
    entradas_invalidas = [{"tipo_pase": "VIP", "precio_unitario": 20000}]
    with pytest.raises(ValueError, match="La edad de cada visitante debe estar entre 0 y 99"):
        validar_datos_visitantes(entradas_invalidas)


def test_validar_datos_visitantes_rechaza_edad_mayor_99():
    entradas_invalidas = [{"edad": 100, "tipo_pase": "REGULAR", "precio_unitario": 10000}]
    with pytest.raises(ValueError, match="La edad de cada visitante debe estar entre 0 y 99"):
        validar_datos_visitantes(entradas_invalidas)


# --- TESTS DE PRECIOS ---

def test_precio_regular_adulto():
    assert calcular_precio(30, "REGULAR") == 10000.0

def test_precio_vip_adulto():
    assert calcular_precio(30, "VIP") == 20000.0

def test_precio_menor_3_anios_gratis():
    assert calcular_precio(2, "VIP") == 0.0
    assert calcular_precio(3, "REGULAR") == 0.0

def test_precio_menor_15_anios_descuento_50():
    assert calcular_precio(10, "REGULAR") == 5000.0
    assert calcular_precio(15, "VIP") == 10000.0

def test_precio_mayor_60_anios_descuento_50():
    assert calcular_precio(65, "REGULAR") == 5000.0
    assert calcular_precio(60, "VIP") == 10000.0


# --- TEST DEL CAMINO FELIZ (CON LOOP Y RELACIÓN 1 a N) ---

@pytest.mark.django_db
def test_procesar_compra_exitosa_guarda_con_esquema_completo(fecha_futura):
    # Arrange: Simulamos que en la BD ya existen estos registros básicos
    usuario_real = Usuario.objects.create(nombre="Alexis", apellido="G", email="alexis@test.com")
    forma_tarjeta = FormaPago.objects.create(nombre="TARJETA")
    tipo_vip = TipoEntrada.objects.create(nombre="VIP")
    tipo_regular = TipoEntrada.objects.create(nombre="REGULAR")
   
    datos_compra = {
        "usuario": {"id": usuario_real.id, "nombre": usuario_real.nombre},
        "fecha": fecha_futura,
        "forma_pago": "TARJETA",
        "entradas": [
            {"edad": 25, "tipo_pase": "VIP", "precio_unitario": 20000.0},
            {"edad": 12, "tipo_pase": "REGULAR", "precio_unitario": 10000.0}
        ]
    }
    
    # Act
    compra_procesada = procesar_compra(datos_compra)
    
    assert Compra.objects.count() == 1
    assert Entrada.objects.count() == 2
    assert compra_procesada.cantidad_entradas == 2
    assert compra_procesada.fecha == fecha_futura          # consigna: informar fecha al finalizar
    assert compra_procesada.monto_total == 25000.0  # VIP adulto $20000 + Regular menor15 $5000
    assert compra_procesada.usuario == usuario_real


# --- TESTS DE MERCADO PAGO ---

@pytest.mark.django_db
def test_procesar_compra_con_tarjeta_genera_url_mercado_pago(fecha_futura):
    usuario = Usuario.objects.create(nombre="Ana", apellido="P", email="ana@test.com")
    FormaPago.objects.create(nombre="TARJETA")
    TipoEntrada.objects.create(nombre="REGULAR")

    datos = {
        "usuario": {"id": usuario.id},
        "fecha": fecha_futura,
        "forma_pago": "TARJETA",
        "entradas": [{"edad": 25, "tipo_pase": "REGULAR", "precio_unitario": 10000.0}]
    }
    compra = procesar_compra(datos)

    assert compra.mercado_pago_redirect_url is not None
    assert str(compra.id) in compra.mercado_pago_redirect_url


@pytest.mark.django_db
def test_procesar_compra_con_efectivo_no_tiene_url_mercado_pago(fecha_futura):
    usuario = Usuario.objects.create(nombre="Luis", apellido="Q", email="luis@test.com")
    FormaPago.objects.create(nombre="EFECTIVO")
    TipoEntrada.objects.create(nombre="REGULAR")

    datos = {
        "usuario": {"id": usuario.id},
        "fecha": fecha_futura,
        "forma_pago": "EFECTIVO",
        "entradas": [{"edad": 30, "tipo_pase": "REGULAR", "precio_unitario": 10000.0}]
    }
    compra = procesar_compra(datos)

    assert compra.mercado_pago_redirect_url is None


# --- TEST DE MAIL DE CONFIRMACIÓN ---

@pytest.mark.django_db
def test_procesar_compra_envia_mail_confirmacion(fecha_futura, mailoutbox):
    usuario = Usuario.objects.create(nombre="María", apellido="R", email="maria@test.com")
    FormaPago.objects.create(nombre="EFECTIVO")
    TipoEntrada.objects.create(nombre="REGULAR")

    datos = {
        "usuario": {"id": usuario.id},
        "fecha": fecha_futura,
        "forma_pago": "EFECTIVO",
        "entradas": [{"edad": 25, "tipo_pase": "REGULAR", "precio_unitario": 10000.0}]
    }
    compra = procesar_compra(datos)

    assert len(mailoutbox) == 1
    assert "maria@test.com" in mailoutbox[0].to
    assert fecha_futura.strftime('%d/%m/%Y') in mailoutbox[0].body  # formato dd/mm/YYYY
    assert str(compra.cantidad_entradas) in mailoutbox[0].body
    assert "EcoHarmony Park" in mailoutbox[0].subject