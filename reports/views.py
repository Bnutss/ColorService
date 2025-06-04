import json
import logging
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from django.shortcuts import render

logger = logging.getLogger(__name__)


def get_data_color_service(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST method allowed")

        # Проверка токена
    expected_token = getattr(settings, 'API_TOKEN', 'color_service_supersecret')
    auth_header = request.headers.get('Authorization')

    if not auth_header or auth_header != f"Bearer {expected_token}":
        return HttpResponseForbidden("Invalid or missing token")

    # Обработка JSON
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    # Логирование
    logger.info(f"Received data: {json.dumps(data)[:500]}")  # ограничиваем размер лога

    # Здесь можно сохранить в БД или файл
    return JsonResponse({"status": "ok", "received_records": len(data)})
