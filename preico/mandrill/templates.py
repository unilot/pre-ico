from django.utils.translation import get_language


class Templates:
    USER_VERIFY_EMAIL = 'user-veryfy-email-{locale}'
    USER_READY_TO_BUY = 'user-ready-to-buy-{locale}'
    USER_RESET_PASSWORD = 'user-reset-password-{locale}'

    @classmethod
    def get_template_key(cls, template_name, locale=None):
        template_locale = get_language()

        if not locale is None:
            template_locale = locale

        return template_name.format(locale=template_locale)

