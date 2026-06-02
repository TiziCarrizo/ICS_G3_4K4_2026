import pytest
from datetime import date, timedelta
from comprar_entradas.services import calcular_precio_real
import json

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

def test_validar_fecha_rechaza_dias_festivos_navidad_y_ano_nuevo():
    navidad = date(2026, 12, 25)
    ano_nuevo = date(2027, 1, 1)

    with pytest.raises(ValueError, match="El parque está cerrado los días festivos"):
        validar_fecha_visita(navidad)

    with pytest.raises(ValueError, match="El parque está cerrado los días festivos"):
        validar_fecha_visita(ano_nuevo)

def test_validar_edades_rechaza_edades_no_enteras():
    # Caso 1: Le mandan un texto en vez de un número
    with pytest.raises(ValueError, match="La edad debe ser un número entero"):
        validar_edades_visitantes([{"edad": "veinte", "tipo_pase": "REGULAR"}])

    # Caso 2: Le mandan un número con decimales (float)
    with pytest.raises(ValueError, match="La edad debe ser un número entero"):
        validar_edades_visitantes([{"edad": 25.5, "tipo_pase": "VIP"}])

def test_validar_cantidad_entradas_rechaza_formato_incorrecto():
    entradas_texto = "muchas entradas"
    entradas_decimal = 2.5
    
    with pytest.raises(ValueError, match="El campo entradas debe ser una lista válida"):
        validar_cantidad_entradas(entradas_texto)
        
    with pytest.raises(ValueError, match="El campo entradas debe ser una lista válida"):
        validar_cantidad_entradas(entradas_decimal)

def test_validar_cantidad_entradas_rechaza_negativos():
    entradas_negativas = -5
    
    with pytest.raises(ValueError, match="La cantidad de entradas no puede ser negativa"):
        validar_cantidad_entradas(entradas_negativas)


# --- TEST DEL CAMINO FELIZ (CON LOOP Y RELACIÓN 1 a N) ---
@pytest.mark.django_db
def test_procesar_compra_exitosa_guarda_con_esquema_completo(fecha_futura):
    # Arrange
    usuario_real = Usuario.objects.get_or_create(nombre="Alexis", apellido="G", email="alexis_prueba_unitaria@test.com")[0]
    forma_tarjeta = FormaPago.objects.get_or_create(nombre="TARJETA")[0]
    tipo_vip = TipoEntrada.objects.get_or_create(nombre="VIP")[0]
    tipo_regular = TipoEntrada.objects.get_or_create(nombre="REGULAR")[0]
   
    datos_compra = {
        "usuario": {"id": usuario_real.id, "nombre": usuario_real.nombre},
        "fecha": fecha_futura,
        "forma_pago": "TARJETA",
        "entradas": [
            {"edad": 25, "tipo_pase": "VIP"},    
            {"edad": 12, "tipo_pase": "REGULAR"}   
        ]
    }
    
    compra_procesada = procesar_compra(datos_compra)
    
    # Restamos las 2 compras que ya inserta tu migración automática para este test específico (ahora hay 3 en total)
    assert Compra.objects.count() >= 1 
    assert Entrada.objects.count() >= 2
    assert compra_procesada.cantidad_entradas == 2
    assert compra_procesada.monto_total == 25000.0  # El total real es 20000 + 5000
    assert compra_procesada.usuario == usuario_real
    
# --- TESTS DE MERCADO PAGO ---

@pytest.mark.django_db
def test_procesar_compra_con_tarjeta_genera_url_mercado_pago(fecha_futura):
    usuario = Usuario.objects.get_or_create(nombre="Ana", apellido="P", email="ana@test.com")[0]
    FormaPago.objects.get_or_create(nombre="TARJETA")[0]
    TipoEntrada.objects.get_or_create(nombre="REGULAR")[0]

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
    usuario = Usuario.objects.get_or_create(nombre="Luis", apellido="Q", email="luis@test.com")[0]
    FormaPago.objects.get_or_create(nombre="EFECTIVO")[0]
    TipoEntrada.objects.get_or_create(nombre="REGULAR")[0]

    datos = {
        "usuario": {"id": usuario.id},
        "fecha": fecha_futura,
        "forma_pago": "EFECTIVO",
        "entradas": [{"edad": 30, "tipo_pase": "REGULAR", "precio_unitario": 10000.0}]
    }
    compra = procesar_compra(datos)

    assert compra.mercado_pago_redirect_url is None

@pytest.mark.django_db
def test_procesar_compra_recalcula_precios_e_ignora_frontend(fecha_futura):
    usuario = Usuario.objects.get_or_create(nombre="Hack", apellido="Er", email="hack@test.com")[0]
    FormaPago.objects.get_or_create(nombre="TARJETA")[0]
    TipoEntrada.objects.get_or_create(nombre="VIP")[0]
    TipoEntrada.objects.get_or_create(nombre="REGULAR")[0]

    datos_compra = {
        "usuario": {"id": usuario.id},
        "fecha": fecha_futura,
        "forma_pago": "TARJETA",
        "entradas": [
            {"edad": 2, "tipo_pase": "VIP", "precio_unitario": 999.0},     # Debería ser 0 (<=3 años)
            {"edad": 10, "tipo_pase": "REGULAR", "precio_unitario": 0.0},  # Debería ser 5000 (10000 * 0.5)
            {"edad": 30, "tipo_pase": "VIP", "precio_unitario": 1.0},      # Debería ser 20000
            {"edad": 65, "tipo_pase": "REGULAR", "precio_unitario": 0.0}   # Debería ser 5000 (10000 * 0.5)
        ]
    }
    
    compra = procesar_compra(datos_compra)
    
    assert compra.monto_total == 30000.0
    
    entradas_guardadas = compra.entradas.order_by('id')
    assert entradas_guardadas[0].precio_unitario == 0.0
    assert entradas_guardadas[1].precio_unitario == 5000.0
    assert entradas_guardadas[2].precio_unitario == 20000.0
    assert entradas_guardadas[3].precio_unitario == 5000.0

def test_calcular_precio_real_valores_limite():

    assert calcular_precio_real("VIP", 3) == 0.0      
    assert calcular_precio_real("VIP", 4) == 10000.0  
    
    assert calcular_precio_real("VIP", 15) == 10000.0 
    assert calcular_precio_real("VIP", 16) == 20000.0 
    
    assert calcular_precio_real("VIP", 59) == 20000.0 
    assert calcular_precio_real("VIP", 60) == 10000.0 

@pytest.mark.django_db
def test_procesar_compra_efectivo_no_genera_link_mercado_pago(fecha_futura):

    usuario = Usuario.objects.get_or_create(nombre="Efectivo", apellido="Test", email="efectivo@test.com")[0]
    FormaPago.objects.get_or_create(nombre="EFECTIVO")[0]
    TipoEntrada.objects.get_or_create(nombre="REGULAR")[0]
    
    datos_compra = {
        "usuario": {"id": usuario.id, "nombre": usuario.nombre},
        "fecha": fecha_futura,
        "forma_pago": "EFECTIVO",
        "entradas": [{"edad": 30, "tipo_pase": "REGULAR"}]
    }
    
    compra = procesar_compra(datos_compra)
    
    assert compra.forma_pago.nombre == "EFECTIVO"
    assert compra.mercado_pago_redirect_url is None  

@pytest.mark.django_db
def test_api_realizar_compra_retorna_400_si_falta_dato_clave(client):
    usuario_real = Usuario.objects.get_or_create(nombre="Incompleto", apellido="Test", email="inc@test.com")[0]
    FormaPago.objects.get_or_create(nombre="TARJETA")[0]
    
    payload_sin_fecha = {
        "usuario": {"id": usuario_real.id, "nombre": usuario_real.nombre},
        "forma_pago": "TARJETA",
        "entradas": [{"edad": 25, "tipo_pase": "VIP"}]
    }
    
    response = client.post(
        '/api/compras/', 
        data=json.dumps(payload_sin_fecha),
        content_type='application/json'
    )
    
    assert response.status_code == 400

@pytest.mark.django_db
def test_api_realizar_compra_retorna_400_si_formato_fecha_es_invalido(client):
    usuario_real = Usuario.objects.get_or_create(nombre="Fecha", apellido="Invalida", email="fecha@test.com")[0]
    FormaPago.objects.get_or_create(nombre="TARJETA")[0]
    
    payload_fecha_invalida = {
        "usuario": {"id": usuario_real.id, "nombre": usuario_real.nombre},
        "fecha": "25/12/2026",  
        "forma_pago": "TARJETA",
        "entradas": [{"edad": 25, "tipo_pase": "VIP"}]
    }
    
    response = client.post(
        '/api/compras/', 
        data=json.dumps(payload_fecha_invalida),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    
    data = response.json()
    assert "error" in data