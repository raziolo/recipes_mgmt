from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ingredients.views import IngredientViewSet
from recipes.views import RecipeViewSet
from production.views import ProductionSessionViewSet, ProductionTaskViewSet

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'production-sessions', ProductionSessionViewSet)
router.register(r'production-tasks', ProductionTaskViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
