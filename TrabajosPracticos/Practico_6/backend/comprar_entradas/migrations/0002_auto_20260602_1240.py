from django.db import migrations
from django.utils import timezone
from datetime import date

def cargar_datos_iniciales(apps, schema_editor):
    # Obtenemos los modelos de esta forma especial para migraciones
    Usuario = apps.get_model('comprar_entradas', 'Usuario')
    TipoEntrada = apps.get_model('comprar_entradas', 'TipoEntrada') # O 'TipoPase'
    FormaPago = apps.get_model('comprar_entradas', 'FormaPago')

    # 1. Cargar Usuarios
    # Usamos get_or_create para que si se corre dos veces, no tire error por duplicado
    Usuario.objects.get_or_create(id=1, nombre="Manuel", apellido="Dávila", email="manuelandresdavila642@gmail.com")
    Usuario.objects.get_or_create(id=2, nombre="Alexis", apellido="Felippa", email="alexis@test.com")

    # 2. Cargar Tipos de Entrada/Pase
    TipoEntrada.objects.get_or_create(id=1, nombre="VIP")
    TipoEntrada.objects.get_or_create(id=2, nombre="Regular")

    # 3. Cargar Formas de Pago
    FormaPago.objects.get_or_create(id=1, nombre="EFECTIVO")
    FormaPago.objects.get_or_create(id=2, nombre="TARJETA")

    # 4. Traer los modelos de Compra y Entrada
    Compra = apps.get_model('comprar_entradas', 'Compra')
    Entrada = apps.get_model('comprar_entradas', 'Entrada')

    # 5. Rescatar las instancias que creamos más arriba
    usuario_manuel = Usuario.objects.get(id=1)
    pago_efectivo = FormaPago.objects.get(id=1)
    pago_tarjeta = FormaPago.objects.get(id=2)
    tipo_vip = TipoEntrada.objects.get(id=1)
    tipo_regular = TipoEntrada.objects.get(id=2)

    # 6. Crear Compra 1: Manuel, EFECTIVO
    # Entradas:
    # 1 VIP de 25 años -> No tiene descuento -> $20.000
    # 1 Regular de 24 años -> No tiene descuento -> $10.000
    # Total de la compra = $30.000
    compra_1, created_1 = Compra.objects.get_or_create(
        id=1,
        defaults={
            'usuario': usuario_manuel,
            'forma_pago': pago_efectivo,
            'fecha': date(2026, 6, 15),
            'fecha_compra': timezone.now(),
            'cantidad_entradas': 2,
            'monto_total': 30000.00,
            'mercado_pago_redirect_url': 'https://www.mercadopago.com.ar/sandbox/init/efectivo123'
        }
    )
    if created_1:
        Entrada.objects.create(edad=25, precio_unitario=20000.00, compra=compra_1, tipo_entrada=tipo_vip)
        Entrada.objects.create(edad=24, precio_unitario=10000.00, compra=compra_1, tipo_entrada=tipo_regular)

    # 7. Crear Compra 2: Manuel, TARJETA
    # Entradas:
    # 1 VIP de 65 años -> Mayor de 60 años (50% off sobre los $20.000) -> $10.000
    # Total de la compra = $10.000
    compra_2, created_2 = Compra.objects.get_or_create(
        id=2,
        defaults={
            'usuario': usuario_manuel,
            'forma_pago': pago_tarjeta,
            'fecha': date(2026, 7, 20),
            'fecha_compra': timezone.now(),
            'cantidad_entradas': 1,
            'monto_total': 10000.00,
            'mercado_pago_redirect_url': 'https://www.mercadopago.com.ar/sandbox/init/tarjeta456'
        }
    )
    if created_2:
        Entrada.objects.create(edad=65, precio_unitario=10000.00, compra=compra_2, tipo_entrada=tipo_vip)

    

def revertir_datos_iniciales(apps, schema_editor):
    # Por si alguna vez necesitamos deshacer la migración
    pass

class Migration(migrations.Migration):

    dependencies = [
        # Acá va a decir de qué migración depende (suele dejarse lo que te generó el comando automáticamente)
        ('comprar_entradas', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(cargar_datos_iniciales, revertir_datos_iniciales),
    ]