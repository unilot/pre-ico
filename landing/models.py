import sys
import uuid

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import images
from django.db import models, transaction
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from hvad.models import TranslatableModel, TranslatedFields
from PIL import Image
from io import FileIO, BytesIO
import os

from preico.validators import ImageMinSizeValidator
from preico import settings


class ResizableImageFieldMixin():
    def __resize_image__(self, image_field, cover_image_path, width, height, format, quality = 100):
        orig_width, orig_height = images.get_image_dimensions(image_field)

        if orig_width > width or orig_height > height:

            im = Image.open(image_field)

            proportioned_height = (height / width) * orig_width
            proportioned_width = (width / height) * orig_height

            #Depending on size of image this section calculates part of image that will be croped
            #before resize to fit correct image proportions
            if proportioned_height < orig_height:
                x0 = 0
                y0 = (orig_height - proportioned_height) / 2
                x1 = orig_width
                y1 = y0 + proportioned_height
            else:
                x0 = (orig_width - proportioned_width) / 2
                y0 = 0
                x1 = x0 + proportioned_width
                y1 = orig_height

            transformed_im = im.transform((width, height),
                                          Image.EXTENT, (x0, y0, x1, y1))

            im.close()

            output = FileIO(cover_image_path, 'w+')
            output.seek(0)
            transformed_im.save(output, format=format, quality=quality)

            transformed_im.close()
            output.close()

    def __process_image__(self, field_name, field, field_config, image_path, is_new):
        file_name = os.path.basename(image_path)

        self.__resize_image__(field, image_path,
                              field_config.get('WIDTH'),
                              field_config.get('HEIGHT'),
                              field_config.get('FORMAT'),
                              field_config.get('QUALITY') or 100)

        # If model save is called for new model file will be created like:
        # {title}.png. But we need it to be saved as: {pk}-{language_code}.png
        # To achive so we'll need emulate file reupload and run second save and
        # remove already uploaded file because after first save we have pk
        if is_new:
            old_file = field.path
            im = Image.open(field)
            output = BytesIO()

            im.save(output, format=field_config.get('FORMAT'),
                    quality=field_config.get('QUALITY') or 100)
            output.seek(0)

            setattr(self, field_name, InMemoryUploadedFile(
                    output,
                    field_name,
                    file_name,
                    'image/%s' % field_config.get('FORMAT').lower(),
                    sys.getsizeof(output),
                    None
                )
            )

            im.close()

            if os.path.exists(old_file):
                os.remove(old_file)


# Couldn't come up with better name
class AdvancedImageFieldsProcessingModelMixin():
    __is_process_extra_save_on_new__ = True

    @classmethod
    def __get_field_config__(cls, field_name):
        config = cls.image_field_params.get(field_name)

        if not config:
            raise RuntimeError(_('Configuration for image field "%s" is not set.' % field_name))
        elif not config.get('WIDTH') or not config.get('HEIGHT') or not config.get('FORMAT') or not config.get('PATH'):
            raise RuntimeError(_('Invalid configuration for field "%s". Field configuration should contain at least: PATH, WIDTH, HEIGHT and FORMAT data.' % field_name))

        return config

    @classmethod
    def __get_image_fields__(cls):
        return cls.image_field_params.keys()

    # I think there is a plenty of room for optimization here.
    # Works fine for now.
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        cover_image_path = {}
        cover_image_tmpfile = {}
        save_path = {}

        for field_name in self.__get_image_fields__():
            config = self.__get_field_config__(field_name)

            save_path[field_name] = config.get('PATH')(self) if callable(config.get('PATH')) else config.get('PATH')

            cover_image_path[field_name] = os.path.join(settings.MEDIA_ROOT, save_path[field_name])
            cover_image_tmpfile[field_name] = '%s.%s' % (cover_image_path[field_name], str(uuid.uuid4()))

        try:
            for field_name in self.__get_image_fields__():
                if os.path.exists(cover_image_path[field_name]):
                    os.rename(cover_image_path[field_name], cover_image_tmpfile[field_name])

            with transaction.atomic():
                is_new = not self.pk
                super(AdvancedImageFieldsProcessingModelMixin, self)\
                    .save(force_insert=force_insert, force_update=force_update,
                                              using=using, update_fields=update_fields)

                for field_name in self.__get_image_fields__():
                    self.__process_image__(field_name,
                                           getattr(self, field_name),
                                           self.__get_field_config__(field_name),
                                           cover_image_path[field_name],
                                           is_new)

                if is_new and self.__is_process_extra_save_on_new__:
                    super(AdvancedImageFieldsProcessingModelMixin, self).save(force_insert=force_insert,
                                                                              force_update=force_update,
                                                                              using=using, update_fields=update_fields)

                for field_name in self.__get_image_fields__():
                    if os.path.exists(cover_image_tmpfile[field_name]) and os.path.exists(cover_image_path[field_name]):
                        os.remove(cover_image_tmpfile[field_name])
                    elif os.path.exists(cover_image_tmpfile[field_name]):
                        os.rename(cover_image_tmpfile[field_name], cover_image_path[field_name])
        except:
            for field_name in self.__get_image_fields__():
                if os.path.exists(cover_image_tmpfile[field_name]):
                    os.rename(cover_image_tmpfile[field_name], cover_image_path[field_name])
            raise


# Create your models here.
class Publication(AdvancedImageFieldsProcessingModelMixin, TranslatableModel, ResizableImageFieldMixin):
    COVER_IMAGE_MIN_WIDTH = 270
    COVER_IMAGE_MIN_HEIGHT = 150
    COVER_IMAGE_FORMAT = 'PNG'
    COVER_IMAGE_PATH = 'landing/publications'

    def __get_cover_image_path__(self, filename=None, only_filename=False):
        file_name = self.pk

        if not file_name:
            file_name = slugify(self.title)

        result = '{filename}-{language_code}.png'\
            .format(filename=file_name, language_code=self.language_code)

        if not only_filename:
            result = os.path.join(Publication.COVER_IMAGE_PATH, result)

        return result

    image_field_params = {
        'cover_image': {
            'WIDTH': COVER_IMAGE_MIN_WIDTH,
            'HEIGHT': COVER_IMAGE_MIN_HEIGHT,
            'FORMAT': COVER_IMAGE_FORMAT,
            'PATH': __get_cover_image_path__,
        }
    }

    translations = TranslatedFields(
        title=models.CharField(max_length=128, null=False, blank=False),
        caption=models.CharField(max_length=512, null=False, blank=False),
        full_url=models.URLField(null=False, blank=False),
        cover_image=models.ImageField(upload_to=__get_cover_image_path__, null=False, blank=True,
                                      validators=(ImageMinSizeValidator(
                                          min_width=COVER_IMAGE_MIN_WIDTH,
                                          min_height=COVER_IMAGE_MIN_HEIGHT),)
                                      ),
        published = models.BooleanField(default=False)
    )

    @property
    def title_(self):
        return self.title


class Roadshow(AdvancedImageFieldsProcessingModelMixin, TranslatableModel, ResizableImageFieldMixin):
    def __get_cover_image_path__(self, *args, **kwargs):
        file_name = self.pk

        if not file_name:
            file_name = slugify(self.title)

        file_name = '{filename}-{language_code}.png'\
            .format(filename=file_name, language_code=self.language_code)

        return os.path.join('landing/roadshow', file_name)

    image_field_params = {
        'cover_image': {
            'WIDTH': 627,
            'HEIGHT': 353,
            'FORMAT': 'PNG',
            'PATH': __get_cover_image_path__,
        }
    }

    translations = TranslatedFields(
        published=models.BooleanField(default=False),
        title=models.CharField(max_length=64, null=False, blank=False),
        location=models.CharField(max_length=32, null=True, blank=False),
        cover_image=models.ImageField(upload_to=__get_cover_image_path__, null=False, blank=False,
                                      validators=(ImageMinSizeValidator(
                                          min_width=image_field_params['cover_image']['WIDTH'],
                                          min_height=image_field_params['cover_image']['HEIGHT']),)
                                      ),
        info_url = models.URLField(null=False, blank=False)
    )

    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=True, blank=True)

    @property
    def title_(self):
        return self.title


class Adviser(AdvancedImageFieldsProcessingModelMixin, TranslatableModel, ResizableImageFieldMixin):
    __is_process_extra_save_on_new__ = False

    def __get_photo_path__(self, *args, **kwargs):
        file_name = '{filename}.png'.format(filename=slugify(self.full_name))

        return os.path.join('landing/adviser', file_name)

    image_field_params = {
        'photo': {
            'WIDTH': 350,
            'HEIGHT': 350,
            'FORMAT': 'PNG',
            'PATH': __get_photo_path__,
        }
    }

    published = models.BooleanField(default=False)
    linkedin_nickname = models.SlugField(max_length=64, null=False, blank=False)
    photo = models.ImageField(upload_to=__get_photo_path__, null=False, blank=False,
                              validators=(ImageMinSizeValidator(
                                        min_width=150,
                                        min_height=150),)
                              )

    translations = TranslatedFields(
        full_name=models.CharField(max_length=32, null=False, blank=False),
        position = models.CharField(max_length=128, null=False, blank=False),
        caption = models.TextField(max_length=1024, null=False, blank=False)
    )

    @property
    def full_name_(self):
        return self.full_name
