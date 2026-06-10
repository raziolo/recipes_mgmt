from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from decimal import Decimal
from .models import Recipe
from .serializers import RecipeSerializer
from .services import RecipeCalculator

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

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
