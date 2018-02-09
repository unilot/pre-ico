import os
from . import settings
from django.utils.translation import get_language, ugettext as _

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

    table_of_content = (
        ('terms', 'Terms and Conditions'),
        ('parties', 'PARTIES TO THESE T&Cs'),
        ('s1', '1. Unilot Platform'),
        ('s2', '2. Scope of T&amp;Cs'),
        ('s3', '3. Purchase Conditions and Restrictions'),
        ('s4', '4. Purchase Periods'),
        ('s5', '5. UNIT Token Price and Bonus Allocation'),
        ('s6', '6. Right to Request Information'),
        ('s7', '7. Creation and Issuance of UNIT Tokens through the Smart Contract System'),
        ('s8', '8. Refunds, Refusals, Suspension and Termination of Contributions'),
        ('s9', '9. Token Functionality'),
        ('s10', '10. Purchaser’s Representations and Warranties'),
        ('s11', '11. Acknowledgement of Risks'),
        ('s12', '12. Audit of the Smart Contract System'),
        ('s13', '13. Security'),
        ('s14', '14. Intellectual Property'),
        ('s15', '15. Indemnity'),
        ('s16', '16. Disclaimers'),
        ('s17', '17. Limitation of Liability'),
        ('s18', '18. Taxation'),
        ('s19', '19. Data Protection'),
        ('s20', '20. Dispute Resolution by Arbitration'),
        ('s21', '21. Miscellaneous'),
        ('schedule1', 'SCHEDULE 1'),
        ('schedule2', 'SCHEDULE 2'),
        ('schedule3', 'SCHEDULE 3'),
    )

    path = os.path.join(settings.BASE_DIR, 'Terms-and-Conditions-Unilot-v1.1.1.html')


class AffiliateTermsAndConditions(Document):
    title = 'Affiliate Terms and Conditions'

    table_of_content = (
        ('affiliate', 'Affiliate Agreement'),
        ('s1', '1. Scope'),
        ('s2', '2. Qualifying Conditions'),
        ('s3', '3. Obligations of the Company'),
        ('s4', '4. Obligations of the Affiliate'),
        ('s5', '5. Payment'),
        ('s6', '6. Termination'),
        ('s7', '7. Warranties'),
        ('s8', '8. Indemnification'),
        ('s9', '9. Company Rights'),
        ('s10', '10. Governing Law &amp; Jurisdiction'),
        ('s11', '11. Assignment'),
        ('s12', '12. Non-Waiver'),
        ('s13', '13. Relationship of the Parties'),
        ('s14', '14. Changes to this Agreement'),
        ('s15', '15. Trademarks'),
        ('schedule1', 'Schedule #1'),
    )

    path = os.path.join(settings.BASE_DIR, 'Affiliate-terms-and-conditions_v1.html')

class BountyProgram(Document):
    title = 'Bounty Program'

    table_of_content = (
        ('bounty', _('Bounty UNILOT')),
        ('bitcointalk', _('Bitcointalk')),
        ('translation-community-management', _('Translation & Community Management')),
        ('facebook', _('Facebook')),
        ('twitter', _('Twitter')),
        ('youtube', _('YouTube')),
        ('reddit', _('Reddit')),
        ('telegram', _('Telegram')),
        ('media-blogs', _('Media and blogs')),
        ('steemit', _('Steemit.com')),
        ('golos', _('Golos.io')),
        ('linkedin', _('Linkedin')),
        ('support', _('Exclusive support')),
        ('reserve', _('Reserve'))
    )

    path = os.path.join(settings.BASE_DIR, 'Bounty-Program-%s.html' % get_language())
