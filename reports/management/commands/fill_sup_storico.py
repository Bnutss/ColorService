import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from reports.models import SupStorico
from django.utils.timezone import now


class Command(BaseCommand):
    help = 'Заполняет SUP_STORICO случайными тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Количество записей для создания')

    def handle(self, *args, **options):
        count = options['count']
        macchine = ['MCH-01', 'MCH-02', 'MCH-03']
        prodotti = ['PRD-001', 'PRD-002', 'PRD-003']
        lotti = ['LOT-A1', 'LOT-B2', 'LOT-C3']
        tank_list = ['TNK-01', 'TNK-02']
        tipo_chiamate = ['AUTO', 'MANUALE']

        for _ in range(count):
            base_time = now() - timedelta(days=random.randint(0, 100))
            data_dosaggio = base_time
            data_inizio = base_time + timedelta(minutes=random.randint(1, 30))
            data_fine = data_inizio + timedelta(minutes=random.randint(10, 60))

            SupStorico.objects.create(
                macchina=random.choice(macchine),
                lotto=random.choice(lotti),
                introduzione=random.randint(1, 100),
                tank=random.choice(tank_list),
                data_dosaggio=data_dosaggio,
                data_inizio=data_inizio,
                data_fine=data_fine,
                id_prodotto=random.choice(prodotti),
                da_dosare=round(random.uniform(10, 50), 2),
                dosato=round(random.uniform(10, 50), 2),
                macchina_cs=random.randint(1, 5),
                linea=random.randint(1, 3),
                tipo_chiamata=random.choice(tipo_chiamate),
                so_number=f"SO-{random.randint(1000, 9999)}",
                po_number=f"PO-{random.randint(1000, 9999)}",
            )

        self.stdout.write(self.style.SUCCESS(f'{count} записей успешно добавлены в SUP_STORICO'))
