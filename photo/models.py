from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Photo(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
