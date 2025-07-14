from django.core.management.base import BaseCommand
from reports.models import TuzRecord, SodaRecord


class Command(BaseCommand):
    help = 'Clears records from TuzRecord and SodaRecord tables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--before-date',
            type=str,
            help='Delete records before this date (format: YYYY-MM-DD)',
        )
        parser.add_argument(
            '--tuz-only',
            action='store_true',
            help='Delete only TuzRecord data',
        )
        parser.add_argument(
            '--soda-only',
            action='store_true',
            help='Delete only SodaRecord data',
        )

    def handle(self, *args, **options):
        before_date = options.get('before_date')
        tuz_only = options['tuz_only']
        soda_only = options['soda_only']

        if tuz_only and soda_only:
            self.stdout.write(
                self.style.ERROR('Cannot use --tuz-only and --soda-only together')
            )
            return

        if not soda_only:
            if before_date:
                try:
                    from datetime import datetime
                    date = datetime.strptime(before_date, '%Y-%m-%d')
                    deleted_tuz_count, _ = TuzRecord.objects.filter(timestamp__lt=date).delete()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully deleted {deleted_tuz_count} TuzRecord(s) before {before_date}')
                    )
                except ValueError:
                    self.stdout.write(
                        self.style.ERROR('Invalid date format. Use YYYY-MM-DD')
                    )
                    return
            else:
                deleted_tuz_count, _ = TuzRecord.objects.all().delete()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully deleted {deleted_tuz_count} TuzRecord(s)')
                )

        if not tuz_only:
            if before_date:
                try:
                    from datetime import datetime
                    date = datetime.strptime(before_date, '%Y-%m-%d')
                    deleted_soda_count, _ = SodaRecord.objects.filter(timestamp__lt=date).delete()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully deleted {deleted_soda_count} SodaRecord(s) before {before_date}')
                    )
                except ValueError:
                    self.stdout.write(
                        self.style.ERROR('Invalid date format. Use YYYY-MM-DD')
                    )
                    return
            else:
                deleted_soda_count, _ = SodaRecord.objects.all().delete()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully deleted {deleted_soda_count} SodaRecord(s)')
                )
