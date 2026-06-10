from decimal import Decimal
from typing import Dict, List, Any
from .models import Recipe, RecipeComponent

class RecipeCalculator:
    @staticmethod
    def calculate(recipe: Recipe, target_qty: Decimal) -> Dict[str, Any]:
        """
        Main entry point for calculation. Returns a structured dict with ingredients and sub-recipes.
        """
        results = {
            'recipe_name': recipe.name,
            'target_qty': float(target_qty),
            'target_unit': recipe.base_yield_unit,
            'ingredients': [],
            'sub_recipes': []
        }

        if recipe.calc_method == 'YIELD':
            scale_factor = target_qty / Decimal(recipe.base_yield_qty)
            for component in recipe.components.all():
                if component.ingredient:
                    results['ingredients'].append({
                        'name': component.ingredient.name,
                        'qty': float(component.value * scale_factor),
                        'unit': component.unit or component.ingredient.unit
                    })
                elif component.sub_recipe:
                    sub_calc = RecipeCalculator.calculate(component.sub_recipe, component.value * scale_factor)
                    results['sub_recipes'].append(sub_calc)

        elif recipe.calc_method == 'PERCENTAGE':
            # Percentage method: component.value is a percentage of target_qty
            for component in recipe.components.all():
                qty = (Decimal(component.value) / Decimal('100')) * target_qty
                if component.ingredient:
                    results['ingredients'].append({
                        'name': component.ingredient.name,
                        'qty': float(qty),
                        'unit': component.unit or component.ingredient.unit
                    })
                elif component.sub_recipe:
                    sub_calc = RecipeCalculator.calculate(component.sub_recipe, qty)
                    results['sub_recipes'].append(sub_calc)

        return results

    @staticmethod
    def flatten_ingredients(calculated_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Flattens a recursive calculation into a single list of base ingredients.
        Useful for a total shopping list or mix list.
        """
        flat_list = []
        
        # Add direct ingredients
        for ing in calculated_data.get('ingredients', []):
            flat_list.append(ing)
            
        # Recurse into sub-recipes
        for sub in calculated_data.get('sub_recipes', []):
            flat_list.extend(RecipeCalculator.flatten_ingredients(sub))
            
        # Consolidate duplicate ingredients
        consolidated = {}
        for item in flat_list:
            key = (item['name'], item['unit'])
            if key in consolidated:
                consolidated[key]['qty'] += item['qty']
            else:
                consolidated[key] = dict(item)
                
        return list(consolidated.values())
