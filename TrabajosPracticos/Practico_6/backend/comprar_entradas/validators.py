# comprar_entradas/validators.py
from datetime import date

def validar_usuario_registrado(usuario):
    if not usuario or "id" not in usuario:
        raise ValueError("El usuario no está registrado")

def validar_fecha_visita(fecha):
    if fecha < date.today():
        raise ValueError("La fecha de visita no puede ser una fecha pasada") 
    if fecha.weekday() == 0:  
        raise ValueError("El parque está cerrado los lunes")
        
    if (fecha.month == 12 and fecha.day == 25) or (fecha.month == 1 and fecha.day == 1):
        raise ValueError("El parque está cerrado los días festivos")

def validar_forma_pago(forma_pago):
    if forma_pago not in ["EFECTIVO", "TARJETA"]:
        raise ValueError("Forma de pago no válida")

def validar_cantidad_entradas(entradas):
    if isinstance(entradas, (int, float)) and entradas < 0:
        raise ValueError("La cantidad de entradas no puede ser negativa")

    if not isinstance(entradas, list):
        raise ValueError("El campo entradas debe ser una lista válida")
        
    if not entradas:
        raise ValueError("Debe ingresar al menos una entrada")
    if len(entradas) > 10:
        raise ValueError("La cantidad de entradas supera el máximo permitido")


def validar_edades_visitantes(entradas):
    for entrada in entradas:
        edad = entrada.get("edad")
        
        if not isinstance(edad, int) or isinstance(edad, bool):
            raise ValueError("La edad debe ser un número entero")
            
        if edad < 0 or edad > 99:
            raise ValueError("La edad del visitante debe estar entre 0 y 99 años")