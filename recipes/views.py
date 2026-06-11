from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from decimal import Decimal
import json
from .models import Recipe
from .serializers import RecipeSerializer
from .services import RecipeCalculator

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_update(self, serializer):
        old = json.loads(json.dumps(self.get_serializer(serializer.instance).data, default=str))
        new = json.loads(json.dumps(serializer.validated_data, default=str))

        def strip_meta(d):
            if isinstance(d, dict):
                d.pop('id', None)
                d.pop('ingredient_name', None)
                d.pop('sub_recipe_name', None)
                for v in d.values():
                    strip_meta(v)
            elif isinstance(d, list):
                for item in d:
                    strip_meta(item)

        strip_meta(old)
        strip_meta(new)

        if old == new:
            return
        serializer.save()

    @action(detail=True, methods=['get'])
    def calculate(self, request, pk=None):
        recipe = self.get_object()
        target_qty = request.query_params.get('qty')
        
        if not target_qty:
            return Response({'error': 'qty parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            target_qty = Decimal(target_qty)
        except:
            return Response({'error': 'Invalid qty'}, status=status.HTTP_400_BAD_REQUEST)

        calculated_data = RecipeCalculator.calculate(recipe, target_qty)
        return Response(calculated_data)

    @action(detail=False, methods=['post'])
    def deduce(self, request):
        components_data = request.data.get('components', [])
        if not components_data:
            return Response({'error': 'components list is required'}, status=status.HTTP_400_BAD_REQUEST)

        result = RecipeCalculator.deduce_percentages(components_data)
        return Response(result)
