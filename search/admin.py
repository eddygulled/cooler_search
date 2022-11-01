from django.contrib import admin
from .models import MasterDataFile


# Register your models here.

class MasterDataFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'file_date', 'active')

admin.site.register(MasterDataFile, MasterDataFileAdmin)
