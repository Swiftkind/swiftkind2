import os.path
from io import BytesIO
from PIL import Image as PILImage

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import default_storage as storage

from wagtail.images.models import Image, AbstractImage, AbstractRendition
from unidecode import unidecode


def get_upload_to(self, filename):
    folder_name = 'original_images'
    filename = self.file.field.storage.get_valid_name(filename)

    # do a unidecode in the filename and then
    # replace non-ascii characters in filename with _ , to sidestep issues with filesystem encoding
    filename = "".join((i if ord(i) < 128 else '_') for i in unidecode(filename))

    # # Truncate filename so it fits in the 100 character limit
    # # https://code.djangoproject.com/ticket/9893
    full_path = os.path.join(folder_name, filename)
    if len(full_path) >= 95:
        chars_to_trim = len(full_path) - 94
        prefix, extension = os.path.splitext(filename)
        filename = prefix[:-chars_to_trim] + extension
        full_path = os.path.join(folder_name, filename)

    return full_path


class SwiftkindImage(AbstractImage):
    """
    Image Model - Custom
    """

    file = models.ImageField(
        verbose_name=_('file'), upload_to=get_upload_to, width_field='width', height_field='height'
    )

    admin_form_fields = Image.admin_form_fields + ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._disable_signals = False

    def save_without_signals(self):
        """
        This allows for updating the model from code running inside post_save()
        signals without going into an infinite loop:
        """
        self._disable_signals = True
        self.save()
        self._disable_signals = False

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # Opening the uploaded image
        old_obj = None
        if self.pk:
            old_obj = SwiftkindImage.objects.get(pk=self.pk)

        hires_output = []

        for x in range(3):
            hires_output.append(BytesIO())

        hires_img = PILImage.open(self.file)

        width = hires_img.size[0]
        height = hires_img.size[1]

        for x in range(3):
            BASE_WIDTH = hires_img.size[0]*((3-x)/3)
            BASE_HEIGHT = hires_img.size[1]*((3-x)/3)

            width = int(BASE_WIDTH)
            height = int(BASE_HEIGHT)
            rendition = hires_img.resize((width, height), PILImage.ANTIALIAS)
            rendition.save(hires_output[x], format=hires_img.format, quality=90)

        super(SwiftkindImage, self).save(force_insert, force_update, using, update_fields)

        # Create a 1x and 2x Rendition
        same_name = old_obj and getattr(old_obj.file, 'name') == self.file.name

        if not old_obj or not same_name:
            rendition_original = self.get_rendition('original')
            rendition_url = rendition_original.url

            file_name = os.path.join('images', rendition_url.split('/')[-1])

            for x in range(3):
                rend_name = '@'+str(3-x)+'x'
                if x==2:
                    rend_name = ''

                if hires_img.format == 'JPEG':
                    hires_img.format = 'JPG'

                rendition_name = '{}.original{}.{}'.format(file_name.split('.')[0],
                                                        rend_name,hires_img.format.lower())

                image_path = storage.open(rendition_name, 'wb')
                image_path.write(hires_output[x].getvalue())
                hires_output[x].seek(0)
                image_path.close()
    

class SwiftkindRendition(AbstractRendition):
    """
    Rendition Model - Custom
    """

    image = models.ForeignKey(SwiftkindImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        """
        Meta props
        """

        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )