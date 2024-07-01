from django.db import models


class Apps(models.Model):
    name = models.CharField(max_length=50)


class Stats(models.Model):
    id = models.ForeignKey(Apps, on_delete=models.CASCADE, primary_key=True)
    student_regs = models.IntegerField()
    student_sends = models.IntegerField()
