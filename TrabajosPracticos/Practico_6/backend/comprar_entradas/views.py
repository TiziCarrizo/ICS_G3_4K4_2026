import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .services import procesar_compra

@csrf_exempt
def api_realizar_compra(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        datos = json.loads(request.body)
        
        # Parseo de fecha
        if "fecha" in datos and isinstance(datos["fecha"], str):
            datos["fecha"] = datetime.strptime(datos["fecha"], "%Y-%m-%d").date()
        
        compra = procesar_compra(datos)
        
        # Armamos la respuesta incluyendo el link de Mercado Pago
        respuesta = {
            "mensaje": "Compra procesada exitosamente",
            "mercado_pago_redirect_url": compra.mercado_pago_redirect_url
        }
        
        return JsonResponse(respuesta, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Formato JSON inválido"}, status=400)
    except ValueError as e:
        # Atrapa errores de validación de negocio (ej. "El parque está cerrado")
        return JsonResponse({"error": str(e)}, status=400)
    except ObjectDoesNotExist:
        # Atrapa errores si no encuentra el Usuario, FormaPago o TipoEntrada en la BD
        return JsonResponse({"error": "Dato paramétrico no encontrado en la base de datos"}, status=404)
    except Exception as e:
        # Un "catch-all" para cualquier otro error imprevisto (evita un 500 feo)
        return JsonResponse({"error": "Error interno del servidor", "detalle": str(e)}, status=500)