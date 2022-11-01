from django.db import models
import os
# Create your models here.


class MasterDataFile(models.Model):
    file_name = models.CharField(max_length=100, verbose_name='Uploaded By')
    file = models.FileField()
    file_date = models.DateTimeField(auto_now=True)
    active  = models.BooleanField(default=False)

    def __str__(self):
        return self.filename()

    def filename(self):
        return os.path.basename(self.file.name)

