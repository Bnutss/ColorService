from django.urls import path
from .views import get_data_color_service, SupStoricoListView, SupStoricoPDFExportView, SupStoricoExcelExportView

app_name = 'reports'
urlpatterns = [
    path('get_data/', get_data_color_service),
    path('list/', SupStoricoListView.as_view(), name='sup_storico_list'),
    path('export/pdf/', SupStoricoPDFExportView.as_view(), name='sup_storico_pdf'),
    path('export/excel/', SupStoricoExcelExportView.as_view(), name='sup_storico_excel'),

]
