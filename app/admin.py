from django.contrib import admin
from .models import *


class CostoStorageAdmin(admin.ModelAdmin):    
    search_fields = ['storage_level','costo',]
    list_display = ['storage_level','dal','al','costo',]
    list_filter = ['dal','al','storage_level',]
    ordering = ['-dal',]
    save_on_top = True
    save_as = True


admin.site.register(CostoStorage,CostoStorageAdmin)

admin.site.site_title = 'Admin'
admin.site.index_title = ''
admin.site.site_header = 'Admin'