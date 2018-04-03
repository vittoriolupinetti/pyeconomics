from django.db import models


class CostoStorage(models.Model):
    dal = models.DateField()
    al = models.DateField()    
    storage_level = models.CharField(max_length=100)
    costo = models.DecimalField(max_digits=14,decimal_places=2)
    class Meta:
        verbose_name_plural = "Costi Storage"
        verbose_name = "Costo Storage"
        