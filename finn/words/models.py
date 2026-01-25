from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Word(models.Model):
    eng = models.CharField(max_length=200)
    fin = models.CharField(max_length=200)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='word'
    )

    def __str__(self):
        return self.eng