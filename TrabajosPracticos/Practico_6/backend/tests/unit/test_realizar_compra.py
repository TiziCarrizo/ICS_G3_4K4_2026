import pytest
from datetime import date, timedelta

try:
    from comprar_entradas.services import (
        validar_usuario_registrado, validar_cantidad_entradas,
        validar_fecha_visita, validar_forma_pago, procesar_compra
    )
  
    from comprar_entradas.validators import (
        validar_usuario_registrado, validar_cantidad_entradas,
        validar_fecha_visita, validar_forma_pago, validar_edades_visitantes
    )

    from comprar_entradas.models import Compra, Entrada, Usuario, FormaPago, TipoEntrada
except ImportError:
    import pytest
    pytest.fail("RED: Faltan definir los nuevos modelos normalizados en models.py")

@pytest.fixture
def fecha_futura():
    return date.today() + timedelta(days=5)


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


def test_validar_forma_pago_rechaza_opcion_invalida():
    pago_invalido = "TRANSFERENCIA"
    with pytest.raises(ValueError, match="Forma de pago no válida"):
        validar_forma_pago(pago_invalido)

def test_validar_edades_rechaza_edades_negativas():
    entradas_invalidas = [{"edad": -1, "tipo_pase": "REGULAR"}]
    with pytest.raises(ValueError, match="La edad del visitante debe estar entre 0 y 99 años"):
        validar_edades_visitantes(entradas_invalidas)

def test_validar_edades_rechaza_edades_mayores_a_99():
    entradas_invalidas = [{"edad": 100, "tipo_pase": "VIP"}]
    with pytest.raises(ValueError, match="La edad del visitante debe estar entre 0 y 99 años"):
        validar_edades_visitantes(entradas_invalidas)


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
            {"edad": 25, "tipo_pase": "VIP", "precio_unitario": 5000.0},
            {"edad": 12, "tipo_pase": "REGULAR", "precio_unitario": 2500.0}
        ]
    }
    
    # Act
    compra_procesada = procesar_compra(datos_compra)
    
    assert Compra.objects.count() == 1
    assert Entrada.objects.count() == 2
    assert compra_procesada.cantidad_entradas == 2
    assert compra_procesada.monto_total == 7500.0 
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