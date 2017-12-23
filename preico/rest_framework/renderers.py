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

# Note, subclass TemplateHTMLRenderer simply for the exception behavior
class JSRenderer(TemplateHTMLRenderer):
    media_type = 'application/javascript'
    format = 'js'

