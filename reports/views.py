import json
import logging
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import SupStorico
from django.views.generic import ListView
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import io
from datetime import datetime

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


class SupStoricoListView(ListView):
    model = SupStorico
    template_name = 'sup_storico/sup_storico_list.html'
    context_object_name = 'records'
    paginate_by = 25

    def get_queryset(self):
        queryset = SupStorico.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(macchina__icontains=search_query) |
                Q(lotto__icontains=search_query) |
                Q(id_prodotto__icontains=search_query) |
                Q(tank__icontains=search_query) |
                Q(so_number__icontains=search_query) |
                Q(po_number__icontains=search_query)
            )

        macchina_filter = self.request.GET.get('macchina')
        if macchina_filter:
            queryset = queryset.filter(macchina=macchina_filter)

        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if date_from:
            queryset = queryset.filter(data_dosaggio__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(data_dosaggio__date__lte=date_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machines'] = SupStorico.objects.values_list('macchina', flat=True).distinct().order_by('macchina')
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_macchina'] = self.request.GET.get('macchina', '')
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')

        return context


class SupStoricoPDFExportView(SupStoricoListView):
    """PDF экспорт с теми же фильтрами"""

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        context = {
            'records': queryset,
            'total_count': queryset.count(),
            'search_query': request.GET.get('search', ''),
            'selected_macchina': request.GET.get('macchina', ''),
            'date_from': request.GET.get('date_from', ''),
            'date_to': request.GET.get('date_to', ''),
            'export_date': datetime.now(),
        }

        template = get_template('sup_storico/pdf_export.html')
        html_string = template.render(context)
        font_config = FontConfiguration()
        html = HTML(string=html_string)
        css = CSS(string='''
            @page {
                size: A4 landscape;
                margin: 1cm;
            }
            body {
                font-family: DejaVu Sans;
                font-size: 10px;
            }
            .table {
                width: 100%;
                border-collapse: collapse;
            }
            .table th, .table td {
                border: 1px solid #ddd;
                padding: 4px;
                text-align: left;
            }
            .table th {
                background-color: #f8f9fa;
                font-weight: bold;
            }
            .badge {
                padding: 2px 6px;
                border-radius: 3px;
                font-size: 9px;
            }
            .bg-primary { background-color: #007bff; color: white; }
            .bg-secondary { background-color: #6c757d; color: white; }
            .bg-success { background-color: #28a745; color: white; }
            .bg-info { background-color: #17a2b8; color: white; }
            .bg-warning { background-color: #ffc107; color: black; }
            .text-center { text-align: center; }
            .fw-bold { font-weight: bold; }
            .small { font-size: 8px; }
        ''', font_config=font_config)

        pdf = html.write_pdf(stylesheets=[css], font_config=font_config)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f'color_service_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response


class SupStoricoExcelExportView(SupStoricoListView):
    """Excel экспорт с теми же фильтрами"""

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "История дозирования"
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center")
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

        headers = [
            'ID', 'Машина', 'Лот', 'Продукт', 'Резервуар',
            'Дата дозирования', 'Время дозирования', 'Дата начала', 'Время начала',
            'Дата окончания', 'Время окончания', 'Количество для дозирования',
            'Дозированное количество', 'Линия', 'SO номер', 'PO номер', 'Тип вызова'
        ]

        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
            cell.border = border

        for row, record in enumerate(queryset, 2):
            data = [
                record.sup_storico_id,
                record.macchina or '',
                record.lotto or '',
                record.id_prodotto or '',
                record.tank or '',
                record.data_dosaggio.date() if record.data_dosaggio else '',
                record.data_dosaggio.time() if record.data_dosaggio else '',
                record.data_inizio.date() if record.data_inizio else '',
                record.data_inizio.time() if record.data_inizio else '',
                record.data_fine.date() if record.data_fine else '',
                record.data_fine.time() if record.data_fine else '',
                record.da_dosare or '',
                record.dosato or '',
                record.linea or '',
                record.so_number or '',
                record.po_number or '',
                record.tipo_chiamata or '',
            ]

            for col, value in enumerate(data, 1):
                cell = ws.cell(row=row, column=col, value=value)
                cell.border = border
                if col in [1, 12, 13, 14]:  # ID, количества, линия
                    cell.alignment = Alignment(horizontal="right")
                elif col in [6, 7, 8, 9, 10, 11]:  # Даты и времена
                    cell.alignment = Alignment(horizontal="center")

        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width

        info_row = len(queryset) + 3
        ws.cell(row=info_row, column=1, value="Параметры экспорта:").font = Font(bold=True)

        if request.GET.get('search'):
            ws.cell(row=info_row + 1, column=1, value=f"Поиск: {request.GET.get('search')}")
        if request.GET.get('macchina'):
            ws.cell(row=info_row + 2, column=1, value=f"Машина: {request.GET.get('macchina')}")
        if request.GET.get('date_from'):
            ws.cell(row=info_row + 3, column=1, value=f"Дата с: {request.GET.get('date_from')}")
        if request.GET.get('date_to'):
            ws.cell(row=info_row + 4, column=1, value=f"Дата по: {request.GET.get('date_to')}")

        ws.cell(row=info_row + 5, column=1, value=f"Дата экспорта: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        ws.cell(row=info_row + 6, column=1, value=f"Всего записей: {queryset.count()}")
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = f'color_service_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response
