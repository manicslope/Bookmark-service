from django.db import models

# Create your models here.
class Bookmark(models.Model):
    username = models.CharField(max_length=200, default="None")
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    favicon = models.CharField(max_length=200)

    def __str__(self):
        return "%s_%s" % (self.username, self.url)
