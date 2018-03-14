from django.contrib import admin
from . import models


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('txn_id', 'user', 'currency', 'amount',)

admin.site.register(models.Transaction, TransactionAdmin)
