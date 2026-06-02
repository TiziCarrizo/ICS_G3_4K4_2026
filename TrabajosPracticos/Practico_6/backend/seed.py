"""
Script para cargar datos iniciales en la BD.
Ejecutar con: py -3.12 manage.py shell < seed.py
"""
from comprar_entradas.models import Usuario, FormaPago, TipoEntrada

FormaPago.objects.get_or_create(nombre="TARJETA")
FormaPago.objects.get_or_create(nombre="EFECTIVO")

TipoEntrada.objects.get_or_create(nombre="VIP")
TipoEntrada.objects.get_or_create(nombre="REGULAR")

u1, _ = Usuario.objects.get_or_create(
    email="chaito109@yahoo.com.ar",
    defaults={"nombre": "Manuel", "apellido": "Dávila"}
)
u2, _ = Usuario.objects.get_or_create(
    email="alexis@test.com",
    defaults={"nombre": "Alexis", "apellido": "Felippa"}
)

print("✓ Datos cargados")
print(f"  Usuario 1 → id={u1.id} | {u1.nombre} {u1.apellido} | {u1.email}")
print(f"  Usuario 2 → id={u2.id} | {u2.nombre} {u2.apellido} | {u2.email}")
