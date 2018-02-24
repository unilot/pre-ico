from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from rest_framework.urlpatterns import format_suffix_patterns

from cp.views import validator, beta_tester
from .views import auth, faq, profile, dashboard, js, affiliate, payment


LOGIN_REDIRECT_URL=reverse_lazy('dashboard', 'html')
LOGIN_URL=reverse_lazy('auth', 'html')
LOGOUT_URL=reverse_lazy('sign-out', 'html')


adoptive_urls = format_suffix_patterns([
    url(r'^faq', faq.FAQView.as_view(), name='faq'),
    url(r'^sign-up', auth.SignUpView.as_view(), name='sign-up'),
    url(r'^(?P<referrer_code>.{32,64})/sign-up', auth.SignUpView.as_view(), name='sign-up-referred'),
    url(r'^sign-in', auth.SignInView.as_view(), name='sign-in'),
    url(r'^sign-out', auth.SignOutView.as_view(), name='sign-out'),
    url(r'^user/(?P<verification_key>.{32})/verify', auth.VerifyEmailView.as_view(), name='verify'),
    url(r'^profile', profile.ProfileView.as_view(), name='profile')
], suffix_required=True, allowed=('json', 'html'))

urlpatterns = format_suffix_patterns([
    url(r'^auth', auth.ShowAuthPageView.as_view(), name='auth'),
    url(r'^(?P<referrer_code>.{32,64})/auth', auth.ShowAuthPageView.as_view(), name='auth-referred'),
    url('^dashboard', dashboard.DashboardView.as_view(), name='dashboard'),
    url('^affiliate', affiliate.AffiliateView.as_view(), name='affiliate'),
], True, ('html',))

urlpatterns += format_suffix_patterns([
    url(r'^validate/user/email', validator.UserEmailValidator.as_view(), name='validate-email'),
    url(r'^validate/user/wallet', validator.UserProfileWalletValidator.as_view(), name='validate-wallet'),
    url(r'^user/password/change', auth.ChangePasswordView.as_view(), name='password-change'),
    url(r'^user/recover', auth.RecoverPassword.as_view(), name='recover-access'),
    url(r'^beta-tester/add', beta_tester.AddBetaTester.as_view(), name='beta-tester'),
    url(r'^user/wallet', profile.WalletView.as_view(), name='user-wallet'),
    url(r'^payment/transaction', payment.CoinPayments.as_view(), name='payment-transaction'),
    url(r'^payment/transaction/(?P<user_id>\d+)/result', payment.CoinPayments.as_view(), name='payment-transaction-result'),
], True, ('json',))

urlpatterns += format_suffix_patterns([
    url(r'^js/config', js.ConfigJsView.as_view(), name='js_config'),
], True, ('js',))

urlpatterns += [
    url('^(|/)$', js.ConfigJsView.as_view(), name='index')
]

urlpatterns += adoptive_urls
