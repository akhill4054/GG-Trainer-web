from django.db import models

# Create your models here.
class Gesture(models.Model):
    data = models.TextField()
    mapped_text = models.CharField(max_length=100)
    rd = models.IntegerField(default=0)
