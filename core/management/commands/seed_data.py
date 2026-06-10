from django.core.management.base import BaseCommand
from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeComponent
from production.models import ProductionSession, ProductionTask
from decimal import Decimal
import datetime

class Command(BaseCommand):
    help = 'Seeds the database with example data'

    def handle(self, *args, **kwargs):
        # 1. Ingredients
        flour = Ingredient.objects.get_or_create(name='Panettone Flour', unit='kg', category='Flour')[0]
        water = Ingredient.objects.get_or_create(name='Water', unit='L', category='Liquid')[0]
        yeast = Ingredient.objects.get_or_create(name='Fresh Yeast', unit='g', category='Leavening')[0]
        semolina = Ingredient.objects.get_or_create(name='Semolina', unit='kg', category='Flour')[0]
        rustico = Ingredient.objects.get_or_create(name='Rustico', unit='kg', category='Flour')[0]
        cereal = Ingredient.objects.get_or_create(name='Cereal Tipo 2', unit='kg', category='Flour')[0]

        # 2. Recipe 1: Biga (Yield Based)
        biga = Recipe.objects.get_or_create(
            name='Biga 100%',
            calc_method='YIELD',
            base_yield_qty=Decimal('3.020'),
            base_yield_unit='kg',
            instructions='Mix roughly. Place in container. Seal with plastic wrap. Refrigerate.'
        )[0]
        
        RecipeComponent.objects.get_or_create(recipe=biga, ingredient=flour, value=Decimal('2.000'), unit='kg')
        RecipeComponent.objects.get_or_create(recipe=biga, ingredient=water, value=Decimal('1.000'), unit='L')
        RecipeComponent.objects.get_or_create(recipe=biga, ingredient=yeast, value=Decimal('20.000'), unit='g')

        # 3. Recipe 2: Flour Mix (Percentage Based)
        flour_mix = Recipe.objects.get_or_create(
            name='House Flour Mix',
            calc_method='PERCENTAGE',
            base_yield_qty=Decimal('1.000'),
            base_yield_unit='kg'
        )[0]
        
        RecipeComponent.objects.get_or_create(recipe=flour_mix, ingredient=semolina, value=Decimal('66.67'))
        RecipeComponent.objects.get_or_create(recipe=flour_mix, ingredient=rustico, value=Decimal('16.67'))
        RecipeComponent.objects.get_or_create(recipe=flour_mix, ingredient=cereal, value=Decimal('16.66'))

        # 4. Production Session
        session = ProductionSession.objects.get_or_create(
            date=datetime.date.today(),
            status='ACTIVE'
        )[0]

        # 5. Production Task
        ProductionTask.objects.get_or_create(
            session=session,
            recipe=biga,
            target_qty=Decimal('6.040'),
            target_unit='kg',
            status='PENDING'
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))
