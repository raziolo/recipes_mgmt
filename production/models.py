from django.db import models
from recipes.models import Recipe

class ProductionSession(models.Model):
    STATUS_CHOICES = [
        ('PLANNED', 'Planned'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
    ]

    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNED')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Session {self.date} ({self.status})"

class ProductionTask(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]

    session = models.ForeignKey(ProductionSession, related_name='tasks', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    target_qty = models.DecimalField(max_digits=10, decimal_places=3)
    target_unit = models.CharField(max_length=10)
    
    # Store calculated result as JSON to preserve history
    calculated_data = models.JSONField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipe.name} - {self.target_qty} {self.target_unit}"
