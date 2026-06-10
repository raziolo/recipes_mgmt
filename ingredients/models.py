from django.db import models

class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('L', 'Liter'),
        ('ml', 'Milliliter'),
        ('pcs', 'Pieces'),
    ]

    name = models.CharField(max_length=255, unique=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='kg')
    category = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
