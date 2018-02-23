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
        document_file = open(cls.path.format(language=get_language()), 'r')

        return document_file.read()


class TermsAndConditions(Document):
    title = _('Terms and Conditions')

    table_of_content = (
        ('terms', _('Terms and Conditions') ),
        ('parties', _('PARTIES TO THESE T&Cs') ),
        ('s1', _('1. Unilot Platform') ),
        ('s2', _('2. Scope of T&Cs') ),
        ('s3', _('3. Purchase Conditions and Restrictions') ),
        ('s4', _('4. Purchase Periods') ),
        ('s5', _('5. UNIT Token Price and Bonus Allocation') ),
        ('s6', _('6. Right to Request Information') ),
        ('s7', _('7. Creation and Issuance of UNIT Tokens through the Smart Contract System') ),
        ('s8', _('8. Refunds, Refusals, Suspension and Termination of Contributions') ),
        ('s9', _('9. Token Functionality') ),
        ('s10', _('10. Purchaser’s Representations and Warranties') ),
        ('s11', _('11. Acknowledgement of Risks') ),
        ('s12', _('12. Audit of the Smart Contract System') ),
        ('s13', _('13. Security') ),
        ('s14', _('14. Intellectual Property') ),
        ('s15', _('15. Indemnity') ),
        ('s16', _('16. Disclaimers') ),
        ('s17', _('17. Limitation of Liability') ),
        ('s18', _('18. Taxation') ),
        ('s19', _('19. Data Protection') ),
        ('s20', _('20. Dispute Resolution by Arbitration') ),
        ('s21', _('21. Miscellaneous') ),
        ('schedule1', _('SCHEDULE 1') ),
        ('schedule2', _('SCHEDULE 2') ),
        ('schedule3', _('SCHEDULE 3') ),
    )

    path = os.path.join(settings.BASE_DIR, 'Terms-and-Conditions-Unilot-v1.1.1-{language}.html')


class AffiliateTermsAndConditions(Document):
    title = _( 'Affiliate Terms and Conditions' )

    table_of_content = (
        ('affiliate', _('Affiliate Agreement') ),
        ('s1', _('1. Scope') ),
        ('s2', _('2. Qualifying Conditions') ),
        ('s3', _('3. Obligations of the Company') ),
        ('s4', _('4. Obligations of the Affiliate') ),
        ('s5', _('5. Payment') ),
        ('s6', _('6. Termination') ),
        ('s7', _('7. Warranties') ),
        ('s8', _('8. Indemnification') ),
        ('s9', _('9. Company Rights') ),
        ('s10', _('10. Governing Law &amp; Jurisdiction') ),
        ('s11', _('11. Assignment') ),
        ('s12', _('12. Non-Waiver') ),
        ('s13', _('13. Relationship of the Parties') ),
        ('s14', _('14. Changes to this Agreement') ),
        ('s15', _('15. Trademarks') ),
        ('schedule1', _('Schedule #1') ),
    )

    path = os.path.join(settings.BASE_DIR, 'Affiliate-terms-and-conditions_v1-{language}.html')

class BountyProgram(Document):
    title = _( 'Bounty Program' )

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

    path = os.path.join(settings.BASE_DIR, 'Bounty-Program-{language}.html')
