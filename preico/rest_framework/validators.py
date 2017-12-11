from rest_framework import validators
from django.utils.translation import ugettext as _
from eth_utils import address


class EthWalletValidator(object):
    message = _('Invalid wallet.')

    def __init__(self, message = None):
        self.message = message or self.message

    def __call__(self, value):
        if not address.is_address(value):
            raise validators.ValidationError(self.message, code='invalid')
