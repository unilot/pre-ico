from rest_framework import views, response, permissions
from preico import document


class AffiliateView(views.APIView):
    permission_classes = [ permissions.IsAuthenticated ]
    template_name = 'cp/affiliate.html'

    def get(self, request, *args, **kwargs):
        data = {
            'affiliate': document.AffiliateTermsAndConditions(),
            'bounty': document.BountyProgram()
        }

        return response.Response(data)
