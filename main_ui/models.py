from django.db import models

# Create your models here.
class VideoUpload(models.Model):
    videoFile = models.FileField(upload_to='videos/')

    def __str__(self):
        return str(self.videoFile)

class QueryUpload(models.Model):
    query = models.CharField(max_length=256)

    def __str__(self):
        return str(self.query)