from django.contrib import admin
from .models import M_Genre

# Register your models here.
class M_GenreAdmin(admin.ModelAdmin):
    fields =["name", "deleteflag"]
    list_display=("name","deleteflag")
    list_filter = ('deleteflag',)

# admin pageで編集できるように設定
admin.site.register(M_Genre, M_GenreAdmin)