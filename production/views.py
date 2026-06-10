from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ProductionSession, ProductionTask
from .serializers import ProductionSessionSerializer, ProductionTaskSerializer
from recipes.services import RecipeCalculator
from printing.services import ProductionSheetPrinter

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
            if not task.calculated_data:
                # Calculate if not already done
                task.calculated_data = RecipeCalculator.calculate(task.recipe, task.target_qty)
                task.save()
            
            # Add instructions safely
            # Ensure task.calculated_data is a dict (JSONField might need refresh)
            data = task.calculated_data
            if not isinstance(data, dict):
                 import json
                 data = json.loads(data) if isinstance(data, str) else {}
            
            data['instructions'] = task.recipe.instructions or "See master recipe."
            
            printer = ProductionSheetPrinter(printer_type='dummy') # Change to usb in production
            printer.print_task(data)
            
            return Response({'status': 'Printed (mocked)', 'output': str(printer.get_output())})
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
