from django.core.management.base import BaseCommand
from django.db.models.query_utils import Q

from cp import models


class Command(BaseCommand):
    help = 'Calculates referral tokens'
    referral_interest_net = (
        0.05,
        0.04,
        0.03,
        0.02,
        0.01
    )

    def handle(self, *args, **options):
        profiles = models.Profile.objects\
            .exclude(Q(token_balance__isnull=True)|Q(token_balance__exact='')|Q(token_balance__exact='0')).all()
        referals = {}

        for profile in profiles:
            referal_level = 0
            referrer = profile.referrer

            if not referrer:
                continue

            for i in range(0, len(self.referral_interest_net) - 1):
                if not referrer:
                    break
                if referrer.id not in referals.keys():
                    referals[referrer.id] = 0

                referals[referrer.id] += ( int(profile.token_balance) / 1.4 ) * self.referral_interest_net[referal_level]

                referrer = referrer.referrer
                referal_level += 1

        for id, referal_balance in referals.items():
            models.Profile.objects.filter(id=id).update(referral_token_balance=int(referal_balance))
