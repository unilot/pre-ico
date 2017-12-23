import os
from . import settings

class Document():
    path=None

    @classmethod
    def get_content(cls):
        document_file = open(cls.path, 'r')

        return document_file.read()


class TermsAndConditions(Document):
    path = os.path.join(settings.BASE_DIR, 'Terms-and-Conditions-Unilot-v1.1.1.md')


class AffiliateTermsAndConditions(Document):
    path = os.path.join(settings.BASE_DIR, 'Affiliate-terms-and-conditions_v1.md')
