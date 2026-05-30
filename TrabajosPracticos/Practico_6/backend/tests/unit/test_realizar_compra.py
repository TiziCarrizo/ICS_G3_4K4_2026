import pytest
from datetime import date, timedelta

try:
    from comprar_entradas.services import (
        validar_usuario_registrado,
        validar_cantidad_entradas,
        validar_fecha_visita,
        validar_forma_pago,
        procesar_compra  
    )
    from comprar_entradas.models import Entrada  
except ImportError:
    pytest.fail("Falta definir procesar_compra en services.py o el modelo Entrada en models.py")


@pytest.fixture
def fecha_futura():
    # Retorna una fecha 5 días en el futuro
    return date.today() + timedelta(days=5)


# --- TESTS RED ---

def test_validar_usuario_rechaza_usuario_no_registrado():
   
    usuario_invalido = {"nombre": "Visitante Anónimo"} # Falta el ID
    
  
    with pytest.raises(ValueError, match="El usuario no está registrado"):
        validar_usuario_registrado(usuario_invalido)


def test_validar_cantidad_entradas_rechaza_mas_de_10():
   
    cantidad_invalida = 11
    
   
    with pytest.raises(ValueError, match="La cantidad de entradas supera el máximo permitido"):
        validar_cantidad_entradas(cantidad_invalida)


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

@pytest.mark.django_db
def test_procesar_compra_exitosa_guarda_en_bd(fecha_futura):
    # Arrange: Un diccionario con datos perfectos que superan todas las validaciones
    datos_compra = {
        "usuario": {"id": 100, "nombre": "Socio Activo"},
        "cantidad": 4,
        "fecha": fecha_futura,
        "forma_pago": "TARJETA"
    }
    
    procesar_compra(datos_compra)
    assert Entrada.objects.count() == 1