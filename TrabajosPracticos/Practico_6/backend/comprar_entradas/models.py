from django.db import models

class Compra(models.Model):
    # El encabezado de la operación
    usuario_id = models.IntegerField()
    fecha_visita = models.DateField()
    forma_pago = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra {self.id} - Usuario {self.usuario_id}"


class Entrada(models.Model):
    # El detalle de cada visitante (N entradas pertenecen a 1 Compra)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='entradas')
    edad = models.IntegerField()
    tipo_pase = models.CharField(max_length=20) 

    def __str__(self):
        return f"Entrada {self.id} ({self.tipo_pase}) - Compra {self.compra.id}"