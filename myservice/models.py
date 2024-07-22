from django.db import models

# Create your models here.
class User(models.Model):
    kakao_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    nickname = models.CharField(max_length=255, null=True, blank=True)