from django.db import models
from .checker import ContentTypeRestrictedFileField
# Create your models here.

SITE_CHOICES = [
    ("ED", "El-Dent"),
    ("WS", "W-Storm"),
    ("RM", "Rocamed"),
    ("AD", "Aveldent")
]

class ProductModel(models.Model):
    name = models.CharField(max_length=255)
    articul = models.CharField(max_length=255)
    price = models.CharField(max_length=10)
    date = models.DateField(auto_now=True)
    site = models.CharField(max_length=2, choices=SITE_CHOICES)
    
    def __str__(self) -> str:
        return f'{self.site} - {self.name} - {self.date}'

class FileModel(models.Model):

    file  = ContentTypeRestrictedFileField(upload_to='uploads/', content_types=['text/csv', 'text/xlsx' ],max_upload_size=5242880 ) 

    def file_path(self):
        return self.file