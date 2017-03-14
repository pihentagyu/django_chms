from django.db import models

# Create your models here.

class Family(models.Model):
    class Meta:
        verbose_name_plural = 'Families'
    created_at = models.DateTimeField(auto_now_add=True)
    family_name = models.CharField(max_length=50)
    address1 = models.CharField(blank=True, max_length=255)
    address2 = models.CharField(blank=True, max_length=255)
    city = models.CharField(blank=True, max_length=50)
    postal_code = models.CharField(blank=True, max_length=10)
    state = models.CharField(blank=True, max_length=50)
    country = models.CharField(blank=True, max_length=70)
    notes = models.TextField(blank=True)
    def __str__(self):
        return self.family_name


