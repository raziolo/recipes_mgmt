from django.db import models
from ingredients.models import Ingredient

class Recipe(models.Model):
    CALC_METHODS = [
        ('PERCENTAGE', 'Percentage (Mix)'),
        ('YIELD', 'Yield (Scaling)'),
    ]

    name = models.CharField(max_length=255, unique=True)
    calc_method = models.CharField(max_length=20, choices=CALC_METHODS, default='YIELD')
    
    # Only used for YIELD method
    base_yield_qty = models.DecimalField(max_digits=10, decimal_places=3, default=1.000)
    base_yield_unit = models.CharField(max_length=10, default='kg')
    
    instructions = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class RecipeComponent(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='components', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT, null=True, blank=True)
    sub_recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT, null=True, blank=True, related_name='used_in')
    
    # value is either percentage (0-100) or absolute quantity
    value = models.DecimalField(max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        name = self.ingredient.name if self.ingredient else self.sub_recipe.name
        return f"{name} in {self.recipe.name}"
