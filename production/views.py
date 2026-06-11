from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ProductionSession, ProductionTask
from .serializers import ProductionSessionSerializer, ProductionTaskSerializer
from recipes.services import RecipeCalculator


class ProductionSessionViewSet(viewsets.ModelViewSet):
    queryset = ProductionSession.objects.all().order_by('-date')
    serializer_class = ProductionSessionSerializer


class ProductionTaskViewSet(viewsets.ModelViewSet):
    queryset = ProductionTask.objects.all()
    serializer_class = ProductionTaskSerializer

    @action(detail=True, methods=['post'])
    def print_sheet(self, request, pk=None):
        try:
            task = self.get_object()
            data = RecipeCalculator.calculate(task.recipe, task.target_qty)
            data['instructions'] = task.recipe.instructions or "See master recipe."
            task.calculated_data = data
            task.save(update_fields=['calculated_data'])
            return Response(data)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def calculate(self, request, pk=None):
        task = self.get_object()
        task.calculated_data = RecipeCalculator.calculate(task.recipe, task.target_qty)
        task.save()
        return Response(task.calculated_data)
