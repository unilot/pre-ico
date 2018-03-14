from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class Transaction(models.Model):
    STATUS_WAITING = 0
    STATUS_COIN_RECEIVED = 1
    STATUS_COMPLETE=100
    STATUS_CANCELLED=-100

    STATUS_LIST = (
        (STATUS_WAITING, _('Waiting for funds')),
        (STATUS_COIN_RECEIVED, _('Coins received. Processing transaction')),
        (STATUS_COMPLETE, _('Transaction complete')),
        (STATUS_CANCELLED, _('Transaction cancelled')),
    )

    user = models.ForeignKey(to=User, null=False, blank=False, editable=False, on_delete=models.deletion.DO_NOTHING,
                              related_name='transactions')
    txn_id = models.CharField(max_length=256, null=False, blank=False, editable=False)
    amount = models.FloatField(null=False, blank=False, editable=False)
    currency = models.CharField(max_length=5, null=False, blank=False, editable=False)
    address = models.CharField(max_length=256, null=False, blank=False, editable=False)
    timeout = models.IntegerField(null=False, blank=False, editable=False)
    status_url = models.URLField(null=False, blank=False, editable=False)
    qrcode_url = models.URLField(null=False, blank=False, editable=False)
    confirms_needed = models.IntegerField(null=False, blank=False, editable=False)
    status = models.IntegerField(choices=STATUS_LIST, null=True, blank=True, default=STATUS_WAITING)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)

