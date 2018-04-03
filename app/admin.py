from django.contrib import admin
from .models import *


class CostoStorageAdmin(admin.ModelAdmin):    
    search_fields = ['servizio','storage_level','costo',]
    list_display = ['servizio','storage_level','dal','al','costo',]
    list_filter = ['dal','al','storage_level','servizio',]
    ordering = ['-dal',]
    save_on_top = True
    save_as = True

class StorageLevelAdmin(admin.ModelAdmin):
    ordering = ['ordine',]
    save_on_top = True
    save_as = True

admin.site.register(CostoStorage,CostoStorageAdmin)
admin.site.register(StorageLevel,StorageLevelAdmin)
admin.site.register(Servizio)

admin.site.site_title = 'Admin'
admin.site.index_title = ''
admin.site.site_header = 'Admin'