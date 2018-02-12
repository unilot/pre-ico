from django.core.management.base import BaseCommand

from landing import models as l_models
from cp import models as c_models

from preico.utils import SendLane


class Command(BaseCommand):
    help = 'Exports leads list to send lane'

    def handle(self, *args, **options):
        subscribers = l_models.Lead.objects\
            .filter(name__isnull=True)\

        for subscriber in subscribers:
            r = SendLane.add_lead(subscriber.email)

            print('%s %s' % (subscriber.email, r.content))

        beta_testers = c_models.BetaTester.objects.all()

        for beta_tester in beta_testers:
            os_type = []

            if beta_tester.is_android:
                os_type.append(2403)

            if beta_tester.is_ios:
                os_type.append(2404)

            if beta_tester.tester:
                name = '%s %s' % (beta_tester.tester.first_name, beta_tester.tester.last_name)
                phone_number = beta_tester.tester.profile.phone_number
            elif beta_tester.lead:
                name = beta_tester.lead.email
                phone_number = beta_tester.lead.phone_number
            else:
                print('Skipping "%s"' % beta_tester.email)
                continue

            r = SendLane.add_beta_tester(beta_tester.email,
                                     name,
                                     phone_number,
                                     os_type)

            print(beta_tester.email, r.content)
