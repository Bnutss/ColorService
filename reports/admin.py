from django.contrib import admin
from .models import SupStorico


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
