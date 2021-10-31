from django.contrib import admin
from django.db.models import fields

from .models import User
# Register your models here.

# admin pageで表示するカラム
class UserAdmin(admin.ModelAdmin):
    fields =["id","name","password", "email"]

# admin pageで編集できるように設定
admin.site.register(User, UserAdmin)
