from unittest import TestCase
from datetime import datetime

from django.core.files.images import ImageFile
from django.conf import settings
from django.test import Client

from .models import FileImage
from .tasks import resize_image
from zipfile import ZipFile
import imghdr


def check_image_type(zipfile: ZipFile):
    for file in zipfile.infolist():
        img = zipfile.open(file)
        if imghdr.what(img) is None:
            return 'fail'
    return 'ok'


class YourTestClass(TestCase):
    def test_post(self):
        c = Client()
        file1 = open(settings.BASE_DIR + '/media/test_images/IMG_2315.jpg', 'rb')
        request = c.post('/upload_file', {'width': 128, 'height': 128, 'file': file1})
        self.assertEqual(request.status_code, 200)

    def test_upload_file(self):
        base_img = open(settings.BASE_DIR+'/media/test_images/IMG_2315.jpg', 'rb')
        new_img = FileImage.objects.create()
        new_img.file.save('IMG_2315.jpg', ImageFile(base_img))
        w = new_img.width
        h = new_img.height
        file = new_img.file.path
        result = resize_image.delay([file], w, h, str(datetime.now()))
        self.assertEqual(check_image_type(ZipFile(settings.BASE_DIR+result.get()['archive_path'])), 'ok', 1)
        self.assertTrue(result.successful())

    def test_incorrect_file(self):
        base_img = open(settings.BASE_DIR + '/media/test_images/incorrect_file.jpg', 'rb')
        new_img = FileImage.objects.create()
        new_img.file.save('incorrect_file.jpg', ImageFile(base_img))
        w = new_img.width
        h = new_img.height
        file = new_img.file.path
        result = resize_image.delay([file], w, h, str(datetime.now()))
        self.assertEqual(check_image_type(ZipFile(settings.BASE_DIR + result.get()['archive_path'])), 'ok', 1)
        self.assertTrue(result.successful())

    def test_incorrect_file_plus_normal_file(self):
        base_img1 = open(settings.BASE_DIR + '/media/test_images/IMG_2315.jpg', 'rb')
        base_img2 = open(settings.BASE_DIR + '/media/test_images/incorrect_file.jpg', 'rb')
        new_img1 = FileImage.objects.create()
        new_img2 = FileImage.objects.create()
        new_img1.file.save('IMG_2315.jpg', ImageFile(base_img1))
        new_img2.file.save('incorrect_file.jpg', ImageFile(base_img2))
        w = new_img1.width
        h = new_img1.height
        file1 = new_img1.file.path
        file2 = new_img2.file.path
        result = resize_image.delay([file1, file2], w, h, str(datetime.now()))
        self.assertEqual(check_image_type(ZipFile(settings.BASE_DIR + result.get()['archive_path'])), 'ok', 1)
        self.assertTrue(result.successful())