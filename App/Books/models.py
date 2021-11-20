from django.db import models
from django import utils

# Create your models here.
class M_Genre(models.Model):
    """
    お気に入り登録できるジャンルの情報を保持するモデル
    """
    id=models.AutoField(primary_key=True)
    name = models.TextField(null=False, blank=False,unique=True)
    insertdate = models.DateField(default=utils.timezone.now)
    updatedate = models.DateField(default=utils.timezone.now)
    deleteflag = models.BooleanField(default=False)