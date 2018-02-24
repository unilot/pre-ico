from hvad.contrib.restframework import TranslatableModelSerializer
from .. import models


class SimpleFaqSerializer(TranslatableModelSerializer):
    class Meta:
        model = models.FAQ
        fields = ( 'id', 'question', 'answer' )
