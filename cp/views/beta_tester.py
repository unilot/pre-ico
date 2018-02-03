from rest_framework import generics, mixins, permissions, response, status
from ..serializers import beta_tester
from .. import models


class AddBetaTester(generics.GenericAPIView, mixins.CreateModelMixin):
    permission_classes = ( permissions.IsAuthenticated, )
    serializer_class = beta_tester.SimpleBetaTesterSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        data['tester'] = request.user.pk

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        beta_tester_qs = models.BetaTester.objects\
            .filter(email=data.get('email'))

        if beta_tester_qs.exists():
            beta_tester_qs.update(tester=request.user.pk)
        else:
            self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
