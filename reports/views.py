import json
import logging
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from ColorService.reports.models import SupStorico


logger = logging.getLogger('django')

@csrf_exempt
def get_data_color_service(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST method allowed")

    expected_token = getattr(settings, 'API_TOKEN', 'color_service_supersecret')
    auth_header = request.headers.get('Authorization')

    if not auth_header or auth_header != f"Bearer {expected_token}":
        return HttpResponseForbidden("Invalid or missing token")

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    logger.info(f"Received data: {json.dumps(data)[:500]}")

    # Очистка таблицы
    SupStorico.objects.all().delete()

    # Создание экземпляров модели
    objects_to_create = []
    for item in data:
        obj = SupStorico(
            sup_storico_id=item.get("SUP_Storico_id"),
            macchina=item.get("Macchina"),
            lotto=item.get("Lotto"),
            introduzione=item.get("Introduzione"),
            tank=item.get("Tank"),
            data_dosaggio=item.get("Data_Dosaggio"),
            data_inizio=item.get("Data_Inizio"),
            data_fine=item.get("Data_Fine"),
            id_prodotto=item.get("ID_Prodotto"),
            da_dosare=item.get("DaDosare"),
            dosato=item.get("Dosato"),
            macchina_cs=item.get("MacchinaCS"),
            linea=item.get("Linea"),
            tipo_chiamata=item.get("TipoChiamata"),
            so_number=item.get("SOnumber"),
            po_number=item.get("POnumber")
        )
        objects_to_create.append(obj)

    SupStorico.objects.bulk_create(objects_to_create, batch_size=1000)

    return JsonResponse({
        "status": "ok",
        "cleared": True,
        "inserted_records": len(objects_to_create)
    })
