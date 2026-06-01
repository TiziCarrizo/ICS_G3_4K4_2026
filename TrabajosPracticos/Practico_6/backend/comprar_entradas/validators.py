# comprar_entradas/validators.py
from datetime import date

def validar_usuario_registrado(usuario):
    if not usuario or "id" not in usuario:
        raise ValueError("El usuario no está registrado")

def validar_cantidad_entradas(entradas):
    if not entradas or len(entradas) > 10:
        raise ValueError("La cantidad de entradas supera el máximo permitido")

def validar_fecha_visita(fecha):
    if fecha < date.today():
        raise ValueError("La fecha de visita no puede ser una fecha pasada") 
    if fecha.weekday() == 0:  
        raise ValueError("El parque está cerrado los lunes")

def validar_forma_pago(forma_pago):
    if forma_pago not in ["EFECTIVO", "TARJETA"]:
        raise ValueError("Forma de pago no válida")

def validar_tipo_pase(tipo_pase):
    if tipo_pase not in ["VIP", "REGULAR"]:
        raise ValueError("Tipo de pase no válido")

def validar_datos_visitantes(entradas):
    for entrada in entradas:
        if "edad" not in entrada or not isinstance(entrada["edad"], (int, float)) or entrada["edad"] <= 0:
            raise ValueError("La edad de cada visitante es obligatoria y debe ser mayor a 0")