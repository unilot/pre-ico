import os
from . import settings

class Document():
    path=None

    @classmethod
    def get_title(cls):
        if not hasattr(cls, 'title'):
            raise NotImplementedError('Declare title attribute')

        return cls.title

    @classmethod
    def get_content(cls):
        document_file = open(cls.path, 'r')

        return document_file.read()


class TermsAndConditions(Document):
    title = 'Terms and Conditions'

    path = os.path.join(settings.BASE_DIR, 'Terms-and-Conditions-Unilot-v1.1.1.html')


class AffiliateTermsAndConditions(Document):
    title = 'Affiliate Terms and Conditions'

    path = os.path.join(settings.BASE_DIR, 'Affiliate-terms-and-conditions_v1.html')


class BountyProgram(Document):
    title = 'Bounty Program'

    path = os.path.join(settings.BASE_DIR, 'Bounty-Program.html')
