from django.db import models

        
class StorageLevel(models.Model):
    nome = models.CharField(max_length=100)
    ordine = models.PositiveIntegerField()
    class Meta:
        ordering = ['ordine']
    def __str__(self):
        return self.nome

class Servizio(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name_plural = "Servizi"
        

class CostoStorage(models.Model):
    dal = models.DateField()
    al = models.DateField()    
    servizio = models.ForeignKey(Servizio,null=True,on_delete=models.SET_NULL)
    storage_level = models.ForeignKey(StorageLevel,null=True,on_delete=models.SET_NULL)
    costo = models.DecimalField(max_digits=14,decimal_places=2)
    class Meta:
        verbose_name_plural = "Costi Storage"
        verbose_name = "Costo Storage"
        
        

