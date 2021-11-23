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

class T_Record(models.Model):
    """
    本の感想を登録しておくモデル。
    """
    username = models.TextField(null=False, blank=False)
    title = models.TextField(null=False, blank=False)
    readdate = models.DateField(null=False, blank=False, default=utils.timezone.now)
    thoughts = models.TextField(null=False, blank=True, default="")
    readflag = models.BooleanField(default=True)
    insertdate = models.DateField(default=utils.timezone.now)
    updatedate = models.DateField(default=utils.timezone.now)
    deleteflag = models.BooleanField(default=False)

    class Meta:
        constraints = [
           # 複合キーが駄目っぽいので、でユニーク制約でそれっぽくする
           models.UniqueConstraint(fields=['username', 'title'], name='unique_T_Record')
       ]