from django.db import models


class SupStorico(models.Model):
    sup_storico_id = models.AutoField(primary_key=True, verbose_name='ID записи')
    macchina = models.CharField(max_length=20, blank=True, null=True, verbose_name='Машина')
    lotto = models.CharField(max_length=20, blank=True, null=True, verbose_name='Партия/Лот')
    introduzione = models.SmallIntegerField(blank=True, null=True, verbose_name='Введение')
    tank = models.CharField(max_length=20, blank=True, null=True, verbose_name='Резервуар')
    data_dosaggio = models.DateTimeField(blank=True, null=True, verbose_name='Дата дозирования')
    data_inizio = models.DateTimeField(blank=True, null=True, verbose_name='Дата начала')
    data_fine = models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания')
    id_prodotto = models.CharField(max_length=20, blank=True, null=True, verbose_name='ID продукта')
    da_dosare = models.FloatField(blank=True, null=True, verbose_name='Количество для дозирования')
    dosato = models.FloatField(blank=True, null=True, verbose_name='Дозированное количество')
    macchina_cs = models.SmallIntegerField(blank=True, null=True, verbose_name='ID машины CS')
    linea = models.SmallIntegerField(blank=True, null=True, verbose_name='Линия')
    tipo_chiamata = models.CharField(max_length=50, blank=True, null=True, verbose_name='Тип вызова')
    so_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Номер SO')
    po_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Номер PO')

    class Meta:
        db_table = 'SUP_STORICO'
        verbose_name = 'Запись по ColorService'
        verbose_name_plural = 'Записи по ColorService'
        ordering = ['-data_dosaggio']
        indexes = [
            models.Index(fields=['data_dosaggio']),
            models.Index(fields=['macchina']),
            models.Index(fields=['lotto']),
            models.Index(fields=['id_prodotto']),
        ]

    def __str__(self):
        return f"Дозирование {self.id_prodotto or 'N/A'} - {self.data_dosaggio or 'Без даты'}"
