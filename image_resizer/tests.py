import os
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from config.settings import MEDIA_ROOT
from image_resizer.forms import UploadImageForm, ResizeImageForm
from image_resizer.models import Image
from PIL import Image as pilImage


class UploadImageFormTests(TestCase):
    def test_correct_url(self):
        form = UploadImageForm(data={'url': 'http://www.ru/1.jpg'})
        self.assertTrue(form.is_valid())

    def test_incorrect_url(self):
        form = UploadImageForm(data={'url': 'http://www.ru/1.pdf'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.get('__all__'), ['Invalid extension'])

    def test_empty_fields(self):
        form = UploadImageForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.get('__all__'), ['Please fill one field'])


class ResizeImageFormTests(TestCase):
    def test_correct_size(self):
        form = ResizeImageForm(data={'width': 1, 'height': 2})
        self.assertTrue(form.is_valid())

    def test_negative_width(self):
        form = ResizeImageForm(data={'width': -1, 'height': 2})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.get('width'), ['Input positive number'])

    def test_negative_height(self):
        form = ResizeImageForm(data={'width': 2, 'height': -1})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.get('height'), ['Input positive number'])


class UploadImageTests(TestCase):
    def test_download_image(self):
        self.client.post(reverse('upload'),
                         data={
                             'url': 'https://www.w3.org/People/mimasa/test/imgformat/img/w3c_home.jpg'})
        self.assertIn('w3c_home', str(Image.objects.all()))

    # def test_upload_image(self):
    #     with open('./fixtures/owl.png', 'rb') as file:
    #         test_image = SimpleUploadedFile(file.name, file.read(), content_type='image/png')
    #         self.client.post(reverse('upload'), data={'image': test_image})
    #
    #     self.assertIn('owl', str(Image.objects.all()))
    # TODO: Work only without form.is_valid() check in upload_image() view


def find_file(filename):
    is_create = False
    resized_file = ''
    for file in os.listdir(os.path.join(MEDIA_ROOT, 'images/resized')):
        if filename in file:
            is_create = True
            resized_file = file
            break
    return is_create, os.path.join(MEDIA_ROOT, 'images/resized', resized_file)


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class ResizeImageTests(TestCase):

    def test_resize_image(self):
        self.client.post(reverse('upload'),
                         data={
                             'url': 'https://www.w3.org/People/mimasa/test/imgformat/img/w3c_home.jpg'})
        self.client.post(reverse('resize_image', kwargs={'pk': 1}),
                         data={'width': 100, 'height': 200})
        is_create, resized_file = find_file('100x200_w3c_home')
        image = pilImage.open(resized_file)
        self.assertEqual(image.width, 100)
        self.assertEqual(image.height, 200)
        self.assertTrue(is_create)

    def test_resize_only_width(self):
        self.client.post(reverse('upload'),
                         data={
                             'url': 'https://www.w3.org/People/mimasa/test/imgformat/img/w3c_home.jpg'})
        self.client.post(reverse('resize_image', kwargs={'pk': 1}),
                         data={'width': 100})
        is_create, resized_file = find_file('100x66_w3c_home')
        image = pilImage.open(resized_file)
        self.assertEqual(image.width, 100)
        self.assertEqual(image.height, 66)
        self.assertTrue(is_create)

    def test_resize_only_height(self):
        self.client.post(reverse('upload'),
                         data={
                             'url': 'https://www.w3.org/People/mimasa/test/imgformat/img/w3c_home.jpg'})
        self.client.post(reverse('resize_image', kwargs={'pk': 1}),
                         data={'height': 100})
        is_create, resized_file = find_file('150x100_w3c_home')
        image = pilImage.open(resized_file)
        self.assertEqual(image.width, 150)
        self.assertEqual(image.height, 100)
        self.assertTrue(is_create)
