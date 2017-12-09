from rest_framework.renderers import TemplateHTMLRenderer as OrigTemplateHTMLRenderer
from rest_framework.utils.serializer_helpers import ReturnList


class TemplateHTMLRenderer(OrigTemplateHTMLRenderer):
    def get_template_context(self, data, renderer_context):
        response = renderer_context['response']
        if response.exception:
            data['status_code'] = response.status_code

        if isinstance(data, ReturnList):
            return {'object_list': data}

        return data
