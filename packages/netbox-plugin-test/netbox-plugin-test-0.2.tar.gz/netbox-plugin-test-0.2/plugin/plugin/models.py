from django.db import models

class DeviceInfo(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    mac = models.CharField(max_length=100)