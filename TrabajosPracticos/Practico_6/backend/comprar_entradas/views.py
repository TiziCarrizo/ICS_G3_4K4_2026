import json
from datetime import date
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .services import procesar_compra
from .models import Usuario


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
        except Exception:
            return JsonResponse({"error": "Error interno del servidor"}, status=500)


class UsuariosView(View):
    def get(self, request):
        usuarios = list(Usuario.objects.values('id', 'nombre', 'apellido', 'email'))
        return JsonResponse(usuarios, safe=False)
