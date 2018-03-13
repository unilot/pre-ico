from django.db import models


class Transaction(models.Model):
    txn_id = models.CharField(max_length=256, null=False, blank=False, editable=False)
    amount = models.FloatField(null=False, blank=False, editable=False)
    currency1 = models.CharField(max_length=5, null=False, blank=False, editable=False)
    currency2 = models.CharField(max_length=5, null=False, blank=False, editable=False)
    buyer_email = models.CharField(max_length=256, null=False, blank=False, editable=False)
    buyer_name = models.CharField(max_length=128, null=False, blank=False, editable=False)
    address = models.CharField(max_length=256, null=False, blank=False, editable=False)
    timeout = models.IntegerField(null=False, blank=False, editable=False)
    status_url = models.URLField(null=False, blank=False, editable=False)
    qrcode_url = models.URLField(null=False, blank=False, editable=False)
    confirms_needed = models.IntegerField(null=False, blank=False, editable=False)
    status = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)

