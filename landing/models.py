from django.db import models


class FileImage(models.Model):
    file = models.ImageField(upload_to='documents/')
    height = models.PositiveSmallIntegerField(default=128)
    width = models.PositiveSmallIntegerField(default=128)
    uploaded_at = models.DateTimeField(auto_now_add=True)
