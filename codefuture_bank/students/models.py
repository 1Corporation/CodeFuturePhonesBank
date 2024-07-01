from django.db import models


class Students(models.Model):
    telegram_id = models.IntegerField(primary_key=True, unique=True)
    username = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    fcs = models.CharField(max_length=100)

