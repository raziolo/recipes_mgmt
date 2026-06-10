from rest_framework import serializers
from .models import ProductionSession, ProductionTask
from recipes.serializers import RecipeSerializer

class ProductionTaskSerializer(serializers.ModelSerializer):
    recipe_name = serializers.ReadOnlyField(source='recipe.name')

    class Meta:
        model = ProductionTask
        fields = '__all__'

class ProductionSessionSerializer(serializers.ModelSerializer):
    tasks = ProductionTaskSerializer(many=True, read_only=True)

    class Meta:
        model = ProductionSession
        fields = '__all__'
