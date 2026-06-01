import json
from datetime import date
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .services import procesar_compra
from .models import Usuario, Compra


@method_decorator(csrf_exempt, name='dispatch')
class ComprarEntradaView(View):

    def post(self, request):
        try:
            body = json.loads(request.body)
            fecha_str = body.get("fecha")
            body["fecha"] = date.fromisoformat(fecha_str)

            compra = procesar_compra(body)

            return JsonResponse({
                "id": compra.id,
                "cantidad_entradas": compra.cantidad_entradas,
                "fecha": str(compra.fecha),
                "monto_total": compra.monto_total,
                "mercado_pago_redirect_url": compra.mercado_pago_redirect_url,
            }, status=201)

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            import traceback
            print(f"[500 ERROR] {type(e).__name__}: {e}")
            traceback.print_exc()
            return JsonResponse({"error": "Error interno del servidor"}, status=500)


class UsuariosView(View):
    def get(self, request):
        usuarios = list(Usuario.objects.values('id', 'nombre', 'apellido', 'email'))
        return JsonResponse(usuarios, safe=False)


class MisComprasView(View):
    def get(self, request):
        usuario_id = request.GET.get('usuario_id')
        if not usuario_id:
            return JsonResponse({"error": "Falta usuario_id"}, status=400)
        compras = (
            Compra.objects
            .filter(usuario_id=usuario_id)
            .prefetch_related('entradas__tipo_entrada')
            .select_related('forma_pago')
            .order_by('-fecha_compra')
        )
        data = []
        for c in compras:
            data.append({
                "id": c.id,
                "fecha": str(c.fecha),
                "fecha_compra": str(c.fecha_compra),
                "cantidad_entradas": c.cantidad_entradas,
                "monto_total": c.monto_total,
                "forma_pago": c.forma_pago.nombre,
                "mercado_pago_redirect_url": c.mercado_pago_redirect_url,
                "entradas": [
                    {"edad": e.edad, "tipo": e.tipo_entrada.nombre, "precio_unitario": e.precio_unitario}
                    for e in c.entradas.all()
                ]
            })
        return JsonResponse(data, safe=False)
