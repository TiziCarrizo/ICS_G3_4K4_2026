from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"


class FormaPago(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class TipoEntrada(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    fecha = models.DateField()
    fecha_compra = models.DateTimeField(auto_now_add=True)
    cantidad_entradas = models.IntegerField()
    monto_total = models.FloatField()
    forma_pago = models.ForeignKey(FormaPago, on_delete=models.RESTRICT)
    usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
    mercado_pago_redirect_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Compra {self.id} - Usuario {self.usuario.nombre} - Total: ${self.monto_total}"


class Entrada(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='entradas')
    edad = models.IntegerField()
    tipo_entrada = models.ForeignKey(TipoEntrada, on_delete=models.RESTRICT)
    precio_unitario = models.FloatField()

    def __str__(self):
        return f"Entrada {self.id} ({self.tipo_entrada.nombre}) - Compra {self.compra.id}"