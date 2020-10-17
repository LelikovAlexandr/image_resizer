from PIL import Image as pilImage

from django.core.files import File
from django.db import models
from django.urls import reverse
import os
import requests
import tempfile

from config.settings import MEDIA_ROOT, MEDIA_URL


class Image(models.Model):
    image = models.ImageField(upload_to='images/', blank=True)

    def get_absolute_url(self):
        return reverse('resize_image', kwargs={'pk': self.pk})

    def download_image(self, url):
        image = requests.get(url).content
        with tempfile.TemporaryFile() as temp_file:
            temp_file.write(image)
            self.image.save(url.split('/')[-1], File(temp_file))

    def get_resized_image_url(self, width, height):
        image = pilImage.open(self.image.path)

        if not width:
            width = int(image.width / (image.height / height))
        if not height:
            height = int(image.height / (image.width / width))

        resized_image = image.resize((width, height))
        file = self.image.path.split('/')[-1]
        if not os.path.exists(os.path.join(MEDIA_ROOT, 'images/resized')):
            os.makedirs(os.path.join(MEDIA_ROOT, 'images/resized'))
        with open(os.path.join(MEDIA_ROOT, 'images/resized', f'{width}x{height}_{file}'),
                  'wb') as resized:
            resized_image.save(resized)
        return os.path.join(MEDIA_URL, 'images/resized', resized.name.split('/')[-1])

    def __str__(self):
        return self.image.path.split('/')[-1]
