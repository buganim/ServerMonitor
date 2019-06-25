from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Server(models.Model):
    server_name = models.CharField(max_length=50)
    server_ip = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="gallery")

    def __str__(self):
        return self.server_name

    class Meta:
        unique_together = ("server_name", "server_ip")
