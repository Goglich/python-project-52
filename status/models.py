from django.db import models

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add=True)