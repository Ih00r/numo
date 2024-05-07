from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Advertisement(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    id = models.AutoField(primary_key=True)


    def __str__(self):
        return self.title
