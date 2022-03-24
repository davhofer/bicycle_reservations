from django.db import models

# Create your models here.
class Values(models.Model):
    name = models.CharField(max_length=20)
    val = models.IntegerField()


class Datapoint(models.Model):
    desc = models.CharField(max_length=50)
    x = models.FloatField()
    y = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

