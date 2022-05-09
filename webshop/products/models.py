from django.urls import reverse

from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10)
    price = models.FloatField()
    description = models.TextField()
    
    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])

