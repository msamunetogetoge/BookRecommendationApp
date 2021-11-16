from django.db import  models
from django import utils
import datetime

from django.db.models import base

# Create your models here.
class M_User(models.Model):
    """
    アカウント情報を保持するモデル
    """
    id = models.TextField(primary_key=True)
    name = models.TextField(null=False, blank=False)
    password = models.TextField(null=False, blank=False)
    email= models.EmailField(null=False, blank=True)
    insertdate = models.DateField(default=utils.timezone.now)
    updatedate = models.DateField(default=utils.timezone.now)
    deleteflag = models.BooleanField(default=False)

class T_Attr(models.Model):
    """
    アカウントの属性情報(趣向)を保存するモデル。
    pkey はid,code,srting のつもり
    code はM_Stringのcode。
    """
    index = models.AutoField(primary_key=True)
    id = models.TextField()
    code = models.PositiveIntegerField( default=0)
    string= models.TextField(default="")
    insertdate = models.DateField(default=utils.timezone.now)
    updatedate = models.DateField(default=utils.timezone.now)
    deleteflag = models.BooleanField(default=False)
    class Meta:
        constraints = [
           # 複合キーが駄目っぽいので、でユニーク制約でそれっぽくする
           models.UniqueConstraint(fields=['id', 'code', 'string'], name='unique_stock')
       ]

class M_String(models.Model):
    """
    色々な文字列をdbに保持する為のモデル。
    """
    code = models.PositiveIntegerField(primary_key=True)
    string = models.TextField()
    insertdate = models.DateField(default=utils.timezone.now)
    updatedate = models.DateField(default=utils.timezone.now)
    deleteflag = models.BooleanField(default=False)

