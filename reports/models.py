from django.db import models


class SupStorico(models.Model):
    sup_storico_id = models.AutoField(primary_key=True)
    macchina = models.CharField(max_length=20, blank=True, null=True)
    lotto = models.CharField(max_length=20, blank=True, null=True)
    introduzione = models.SmallIntegerField(blank=True, null=True)
    tank = models.CharField(max_length=20, blank=True, null=True)
    data_dosaggio = models.DateTimeField(blank=True, null=True)
    data_inizio = models.DateTimeField(blank=True, null=True)
    data_fine = models.DateTimeField(blank=True, null=True)
    id_prodotto = models.CharField(max_length=20, blank=True, null=True)
    da_dosare = models.FloatField(blank=True, null=True)
    dosato = models.FloatField(blank=True, null=True)
    macchina_cs = models.SmallIntegerField(blank=True, null=True)
    linea = models.SmallIntegerField(blank=True, null=True)
    tipo_chiamata = models.CharField(max_length=50, blank=True, null=True)
    so_number = models.CharField(max_length=50, blank=True, null=True)
    po_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'SUP_STORICO'
        verbose_name = 'Запись из SUP_STORICO'
        verbose_name_plural = 'Записи из SUP_STORICO'
