from django.contrib import admin
from django.db.models import fields

from .models import M_User, M_String
# Register your models here.

# admin pageで表示するカラム
class M_UserAdmin(admin.ModelAdmin):
    fields =["username","name","password", "email", "deleteflag"]
    list_filter = ('deleteflag',)

class M_StringAdmin(admin.ModelAdmin):
    fields = ["code", "string", "deleteflag"]
    list_display=("code","string")
    list_filter = ('deleteflag',)

# admin pageで編集できるように設定
admin.site.register(M_User, M_UserAdmin)
admin.site.register(M_String, M_StringAdmin)
