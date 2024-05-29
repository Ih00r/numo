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


class JobAdvertisement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    min_age = models.PositiveIntegerField()
    max_age = models.PositiveIntegerField()
    city = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    danger = models.CharField(
        max_length=1,
        choices=[
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C'),
            ('D', 'D')
        ]
    )

    def __str__(self):
        return self.title