from rest_framework import serializers
from .models import Recipe, RecipeComponent
from ingredients.serializers import IngredientSerializer

class RecipeComponentSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.ReadOnlyField(source='ingredient.name')
    sub_recipe_name = serializers.ReadOnlyField(source='sub_recipe.name')

    class Meta:
        model = RecipeComponent
        fields = ['id', 'ingredient', 'ingredient_name', 'sub_recipe', 'sub_recipe_name', 'value', 'unit']

class RecipeSerializer(serializers.ModelSerializer):
    components = RecipeComponentSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'calc_method', 'base_yield_qty', 'base_yield_unit', 'instructions', 'notes', 'components']
