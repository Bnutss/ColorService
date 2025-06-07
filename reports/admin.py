from django.contrib import admin
from .models import SupStorico, ColorServices
from django import forms
from django.db import transaction
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd


@admin.register(SupStorico)
class SupStoricoAdmin(admin.ModelAdmin):
    list_display = (
        'sup_storico_id', 'macchina', 'lotto', 'introduzione', 'tank',
        'data_dosaggio', 'data_inizio', 'data_fine',
        'id_prodotto', 'da_dosare', 'dosato',
        'macchina_cs', 'linea', 'tipo_chiamata', 'so_number', 'po_number'
    )
    list_filter = ('macchina', 'linea', 'tank', 'id_prodotto')
    search_fields = ('lotto', 'so_number', 'po_number', 'id_prodotto')
    ordering = ('-data_dosaggio',)


class ImportExcelForm(forms.Form):
    excel_file = forms.FileField(label='Excel файл')


@admin.register(ColorServices)
class ColorServicesAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'title', 'type')
    list_filter = ('product_name', 'type')
    search_fields = ('product_name', 'title', 'type')
    ordering = ('product_name',)

    # Добавляем пользовательский URL для импорта
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.admin_site.admin_view(self.import_excel_view),
                 name='colorservices-import-excel'),
        ]
        return custom_urls + urls

    def import_excel_view(self, request):
        if request.method == 'POST':
            form = ImportExcelForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    excel_file = request.FILES['excel_file']
                    df = pd.read_excel(excel_file)

                    # Проверка наличия необходимых колонок
                    required_columns = ['Название продукта', 'Наименование', 'Тип']
                    if not all(col in df.columns for col in required_columns):
                        messages.error(request,
                                       'Excel файл должен содержать колонки: Название продукта, Наименование, Тип')
                        return redirect('..')

                    # Импорт данных
                    with transaction.atomic():
                        created_count = 0
                        for _, row in df.iterrows():
                            ColorServices.objects.update_or_create(
                                product_name=row['Название продукта'],
                                defaults={
                                    'title': row['Наименование'],
                                    'type': row['Тип']
                                }
                            )
                            created_count += 1

                        messages.success(request, f'Успешно импортировано {created_count} записей')
                        return redirect('..')

                except Exception as e:
                    messages.error(request, f'Ошибка при импорте: {str(e)}')
                    return redirect('..')
        else:
            form = ImportExcelForm()

        return render(request, 'admin/import_excel.html', {'form': form})

    def get_actions(self, request):
        actions = super().get_actions(request)
        # Добавляем действие для перехода к форме импорта
        actions['import_excel'] = (self.import_excel_action, 'import_excel', 'Импорт из Excel')
        return actions

    def import_excel_action(self, modeladmin, request, queryset):
        # Перенаправляем на страницу импорта
        return redirect('admin:colorservices-import-excel')
