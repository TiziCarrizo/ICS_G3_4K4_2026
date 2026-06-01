import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import procesar_compra

@csrf_exempt
def api_realizar_compra(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)
            
            if "fecha" in datos and isinstance(datos["fecha"], str):
                datos["fecha"] = datetime.strptime(datos["fecha"], "%Y-%m-%d").date()
            
            compra = procesar_compra(datos)
            
            return JsonResponse({"mensaje": "Compra procesada exitosamente"}, status=201)
            
        except ValueError as e:
            # Atrapamos nuestros errores de validación de negocio y los devolvemos como 400 Bad Request
            return JsonResponse({"error": str(e)}, status=400)
            
    return JsonResponse({"error": "Método no permitido"}, status=405)