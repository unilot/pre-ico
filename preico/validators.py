from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.core.files import images
from django.utils.deconstruct import deconstructible


@deconstructible
class ImageMinSizeValidator(object):
    class ValidationError(ValidationError):
        pass

    message = _('Image is too small. Width should be at least %(min_width)d and height should be at least %(min_height)d')

    def __init__(self, min_width, min_height, message = None):
        self.min_width = min_width
        self.min_height = min_height

        if message:
            self.message = message

    def __call__(self, img):
        width, height = images.get_image_dimensions(img)

        if width < self.min_width or height < self.min_height:
            raise self.__class__.ValidationError(
                self.message % {'min_width':self.min_width, 'min_height': self.min_height}, code='invalid')

    def __eq__(self, o: object) -> bool:
        return ( self.min_width == o.min_width
                 and self.min_height == o.min_height
                 and self.message == o.message)
