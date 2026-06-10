from rest_framework import serializers
from .models import Recipe, RecipeComponent
from ingredients.models import Ingredient
from ingredients.serializers import IngredientSerializer

class RecipeComponentSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.ReadOnlyField(source='ingredient.name')
    sub_recipe_name = serializers.ReadOnlyField(source='sub_recipe.name')

    class Meta:
        model = RecipeComponent
        fields = ['id', 'ingredient', 'ingredient_name', 'sub_recipe', 'sub_recipe_name', 'value', 'unit']

class RecipeSerializer(serializers.ModelSerializer):
    components = RecipeComponentSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'calc_method', 'base_yield_qty', 'base_yield_unit', 'instructions', 'notes', 'components']

    def create(self, validated_data):
        components_data = validated_data.pop('components', [])
        recipe = Recipe.objects.create(**validated_data)
        for component_data in components_data:
            RecipeComponent.objects.create(recipe=recipe, **component_data)
        return recipe

    def update(self, instance, validated_data):
        components_data = validated_data.pop('components', [])
        
        # Update recipe fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Simple approach: clear and recreate components
        # (Better approach would be to track IDs, but this is robust for a local-first app)
        instance.components.all().delete()
        for component_data in components_data:
            RecipeComponent.objects.create(recipe=instance, **component_data)
        
        return instance
