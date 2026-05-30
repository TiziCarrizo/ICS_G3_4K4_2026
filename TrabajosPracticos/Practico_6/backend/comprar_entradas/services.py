from datetime import date

def validar_usuario_registrado(usuario):
    if not usuario or "id" not in usuario:
        raise ValueError("El usuario no está registrado")
    return True

def validar_cantidad_entradas(cantidad):
    if cantidad > 10:
        raise ValueError("La cantidad de entradas supera el máximo permitido")
    return True

def validar_fecha_visita(fecha, feriados=None):
    if fecha < date.today():
        raise ValueError("La fecha de visita no puede ser una fecha pasada")
        
    if fecha.weekday() == 0:  # El índice 0 equivale al lunes
        raise ValueError("El parque está cerrado los lunes")
        
    return True

def validar_forma_pago(forma_pago):
    formas_validas = ["EFECTIVO", "TARJETA"]
    if forma_pago not in formas_validas:
        raise ValueError("Forma de pago no válida")
    return True