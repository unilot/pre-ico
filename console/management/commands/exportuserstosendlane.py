from django.core.management.base import BaseCommand

from django.contrib.auth import models as django_models
from django.db.models.query_utils import Q

from preico.utils import SendLane


class Command(BaseCommand):
    help = 'Exports users with empty balancelist to send lane'

    def handle(self, *args, **options):
        users = django_models.User.objects\
                .filter(beta_tester__isnull=True) \
                .filter(Q(profile__token_balance__isnull=True)
                        | Q(profile__token_balance__exact='')
                        | Q(profile__token_balance__exact='0'))

        for user in users:
            os_type = []

            name = '%s %s' % (user.first_name, user.last_name)
            phone_number = user.beta_tester.profile.phone_number

            r = SendLane.add_beta_tester(user.email,
                                     name,
                                     phone_number,
                                     os_type)

            print(user.email, r.content)
