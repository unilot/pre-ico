from django.core.management.base import BaseCommand
from cp import models


class Command(BaseCommand):
    help = 'Exports beta testers for csv format'

    def add_arguments(self, parser):
        parser.add_argument('start_from', type=int, nargs='?', default=0)

    def handle(self, *args, **options):
        start_from = options.get('start_from')

        if start_from:
            beta_testers_qs = models.BetaTester.objects.filter(id__gte=start_from)
        else:
            beta_testers_qs = models.BetaTester.objects.all()

        for beta_tester in beta_testers_qs:
            name = ''
            email = beta_tester.email
            os = ''

            if beta_tester.tester:
                name = '%s %s' % (beta_tester.tester.first_name, beta_tester.tester.last_name)
            elif beta_tester.lead:
                name = beta_tester.lead.name

            if beta_tester.is_android:
                os = 'Android'

            if beta_tester.is_ios:
                os += ' and IOS' if len(os) > 0 else 'IOS'

            print('"%s";"%s";"%s"' % ( name, email, os ))
