from django.db import models


class GoogleTables(models.Model):
    name = models.CharField(max_length=100)
    sheet_id = models.CharField(max_length=100)
    sheet_name = models.CharField(max_length=100)
    fcs_column = models.IntegerField()
    phone_column = models.IntegerField()
    status_column = models.IntegerField()
