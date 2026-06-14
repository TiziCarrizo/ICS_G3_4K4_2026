import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .services import procesar_compra
from .models import Usuario, Compra


@csrf_exempt
def api_realizar_compra(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        datos = json.loads(request.body)
        
        claves_obligatorias = ["usuario", "fecha", "forma_pago", "entradas"]
        for clave in claves_obligatorias:
            if clave not in datos:
                return JsonResponse({"error": f"Falta el dato obligatorio: {clave}"}, status=400)
        
        if "fecha" in datos and isinstance(datos["fecha"], str):
            datos["fecha"] = datetime.strptime(datos["fecha"], "%Y-%m-%d").date()
        
        compra = procesar_compra(datos)
        
        respuesta = {
            "mensaje": "Compra procesada exitosamente",
            "mercado_pago_redirect_url": compra.mercado_pago_redirect_url
        }
        
        return JsonResponse(respuesta, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Formato JSON inválido"}, status=400)
        
    except KeyError as e:
        # Atrapa si falta 'fecha', 'entradas', 'usuario', etc. en el JSON payload
        return JsonResponse({"error": f"Faltan datos obligatorios en la petición: {str(e)}"}, status=400)
    except ValueError as e:
        # Atrapa errores de validación de negocio (ej. "El parque está cerrado")
        return JsonResponse({"error": str(e)}, status=400) 
    except ObjectDoesNotExist:
        # Atrapa errores si no encuentra el Usuario, FormaPago o TipoEntrada en la BD
        return JsonResponse({"error": "Dato paramétrico no encontrado en la base de datos"}, status=404)
    except Exception as e:
        # Un "catch-all" para cualquier otro error imprevisto (evita un 500 feo)
        return JsonResponse({"error": "Error interno del servidor", "detalle": str(e)}, status=500)

def api_usuarios(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Método no permitido"}, status=405)
    usuarios = list(Usuario.objects.values('id', 'nombre', 'apellido', 'email'))
    return JsonResponse({"usuarios": usuarios})

def api_mis_compras(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Método no permitido"}, status=405)
    usuario_id = request.GET.get('usuario_id')
    if not usuario_id:
        return JsonResponse({"error": "Se requiere usuario_id"}, status=400)
    try:
        compras = Compra.objects.filter(
            usuario_id=usuario_id
        ).prefetch_related('entradas').order_by('-fecha_compra')
        resultado = []
        for compra in compras:
            resultado.append({
                "id": compra.id,
                "fecha": compra.fecha.strftime('%d/%m/%Y'),
                "fecha_compra": compra.fecha_compra.strftime('%d/%m/%Y %H:%M'),
                "cantidad_entradas": compra.cantidad_entradas,
                "monto_total": float(compra.monto_total),
                "forma_pago": compra.forma_pago.nombre,
                "mercado_pago_redirect_url": compra.mercado_pago_redirect_url,
                "entradas": [
                    {"edad": e.edad, "tipo": e.tipo_entrada.nombre, "precio_unitario": float(e.precio_unitario)}
                    for e in compra.entradas.all()
                ]
            })
        return JsonResponse({"compras": resultado})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)