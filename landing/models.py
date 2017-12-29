import sys
import uuid
from pprint import pprint

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import images
from django.db import models, transaction
from django.utils.text import slugify
from hvad.models import TranslatableModel, TranslatedFields
from PIL import Image
from io import FileIO
import os

from preico.validators import ImageMinSizeValidator
from preico import settings


# Create your models here.
class Publication(TranslatableModel):
    COVER_IMAGE_MIN_WIDTH = 270
    COVER_IMAGE_MIN_HEIGHT = 150
    COVER_IMAGE_FORMAT = 'PNG'
    COVER_IMAGE_QUALITY = 100
    COVER_IMAGE_PATH = 'landing/publications'

    def __get_cover_image_path__(self, filename=None, only_filename=False):
        file_name = self.pk

        if not file_name:
            file_name = slugify(self.title)

        result = '{0}.png'.format(file_name)

        if not only_filename:
            result = os.path.join(Publication.COVER_IMAGE_PATH, result)

        return result

    published = models.BooleanField(default=False)
    translations = TranslatedFields(
        title=models.CharField(max_length=128, null=False, blank=False),
        caption=models.CharField(max_length=512, null=False, blank=False),
        full_url=models.URLField(null=False, blank=False),
        cover_image=models.ImageField(upload_to=__get_cover_image_path__, null=False, blank=False,
                                      validators=(ImageMinSizeValidator(
                                          min_width=COVER_IMAGE_MIN_WIDTH,
                                          min_height=COVER_IMAGE_MIN_HEIGHT),)
                                      )
    )

    def title_(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        cover_image_path = os.path.join(settings.MEDIA_ROOT, self.__get_cover_image_path__())
        cover_image_tmpfile = '%s.%s' % (cover_image_path, str(uuid.uuid4()))

        if os.path.exists(cover_image_path):
            os.rename(cover_image_path, cover_image_tmpfile)

        try:
            with transaction.atomic():
                super(Publication, self).save(force_insert=force_insert, force_update=force_insert,
                                              using=using, update_fields=update_fields)

                orig_width, orig_height = images.get_image_dimensions(self.cover_image)


                if orig_width != Publication.COVER_IMAGE_MIN_WIDTH\
                    or orig_height != Publication.COVER_IMAGE_MIN_HEIGHT:

                    im = Image.open(self.cover_image)

                    proportioned_height = (Publication.COVER_IMAGE_MIN_HEIGHT / Publication.COVER_IMAGE_MIN_WIDTH) * orig_width
                    proportioned_width = (Publication.COVER_IMAGE_MIN_WIDTH / Publication.COVER_IMAGE_MIN_HEIGHT) * orig_height

                    if proportioned_height < orig_height:
                        x0 = 0
                        y0 = ( orig_height - proportioned_height ) / 2
                        x1 = orig_width
                        y1 = y0 + proportioned_height
                    else:
                        x0 = ( orig_width - proportioned_width ) / 2
                        y0 = 0
                        x1 = x0 + proportioned_width
                        y1 = orig_height

                    transformed_im = im.transform((self.COVER_IMAGE_MIN_WIDTH, self.COVER_IMAGE_MIN_HEIGHT),
                                      Image.EXTENT, (x0, y0, x1, y1))

                    im.close()

                    output = FileIO(cover_image_path, 'w+')
                    output.seek(0)
                    transformed_im.save(output, format=self.COVER_IMAGE_FORMAT, quality=self.COVER_IMAGE_QUALITY)

                    transformed_im.close()
                    output.close()

                if os.path.exists(cover_image_tmpfile):
                    os.unlink(cover_image_tmpfile)
        except:
            if os.path.exists(cover_image_tmpfile):
                os.rename(cover_image_tmpfile, cover_image_path)
            # Throw error
