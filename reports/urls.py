from django.urls import path
from .views import *

app_name = 'reports'
urlpatterns = [
    path('get_data/', get_data_color_service),
    path('list/', SupStoricoListView.as_view(), name='sup_storico_list'),
    path('export/pdf/', SupStoricoPDFExportView.as_view(), name='sup_storico_pdf'),
    path('export/excel/', SupStoricoExcelExportView.as_view(), name='sup_storico_excel'),
    path("api/import/", import_data),
    path('tuz-records/', TuzRecordListView.as_view(), name='tuz_record_list'),
    path('tuz-records/pdf/', TuzRecordPDFExportView.as_view(), name='tuz_record_pdf'),
    path('tuz-records/excel/', TuzRecordExcelExportView.as_view(), name='tuz_record_excel'),

    path('soda-records/', SodaRecordListView.as_view(), name='soda_record_list'),
    path('soda-records/pdf/', SodaRecordPDFExportView.as_view(), name='soda_record_pdf'),
    path('soda-records/excel/', SodaRecordExcelExportView.as_view(), name='soda_record_excel'),

]
