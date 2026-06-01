"""
Script para cargar datos iniciales de prueba en la BD.
Ejecutar con: py -3.12 manage.py shell < seed.py
"""
from comprar_entradas.models import Usuario, FormaPago, TipoEntrada

# Formas de pago
FormaPago.objects.get_or_create(nombre="TARJETA")
FormaPago.objects.get_or_create(nombre="EFECTIVO")

# Tipos de entrada
TipoEntrada.objects.get_or_create(nombre="VIP")
TipoEntrada.objects.get_or_create(nombre="REGULAR")

# Usuarios de prueba
u1, _ = Usuario.objects.get_or_create(
    email="manuel@test.com",
    defaults={"nombre": "Manuel", "apellido": "Dávila"}
)
u2, _ = Usuario.objects.get_or_create(
    email="alexis@test.com",
    defaults={"nombre": "Alexis", "apellido": "Felippa"}
)

print("✓ Datos de prueba cargados")
print(f"  Usuario 1 → id={u1.id} | {u1.nombre} {u1.apellido} | {u1.email}")
print(f"  Usuario 2 → id={u2.id} | {u2.nombre} {u2.apellido} | {u2.email}")
print(f"  Formas de pago: TARJETA, EFECTIVO")
print(f"  Tipos de entrada: VIP, REGULAR")
