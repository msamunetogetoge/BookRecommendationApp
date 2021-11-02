from django.contrib import admin
from django.db.models import fields

from .models import M_User
# Register your models here.

# admin pageで表示するカラム
class M_UserAdmin(admin.ModelAdmin):
    fields =["id","name","password", "email"]

# admin pageで編集できるように設定
admin.site.register(M_User, M_UserAdmin)
