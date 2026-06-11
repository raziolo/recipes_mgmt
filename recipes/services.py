from decimal import Decimal
from typing import Dict, List, Any
from .models import Recipe, RecipeComponent


def _normalize_to_kg(qty: Decimal, unit: str) -> Decimal:
    if unit in ('kg', 'Kg', 'KG'):
        return qty
    if unit in ('g', 'gr'):
        return qty / Decimal('1000')
    if unit in ('L', 'l'):
        return qty
    if unit in ('ml', 'mL'):
        return qty / Decimal('1000')
    return qty


class RecipeCalculator:
    @staticmethod
    def calculate(recipe: Recipe, target_qty: Decimal) -> Dict[str, Any]:
        results = {
            'recipe_name': recipe.name,
            'target_qty': float(target_qty),
            'target_unit': 'kg',
            'ingredients': [],
            'sub_recipes': []
        }

        components = list(recipe.components.all())
        total_pct = sum(Decimal(c.value) for c in components)
        if total_pct == 0:
            return results

        for component in components:
            qty = (Decimal(component.value) / total_pct) * target_qty
            if component.ingredient:
                results['ingredients'].append({
                    'name': component.ingredient.name,
                    'qty': float(qty),
                    'unit': component.unit or component.ingredient.unit,
                })
            elif component.sub_recipe:
                sub_calc = RecipeCalculator.calculate(component.sub_recipe, qty)
                results['sub_recipes'].append(sub_calc)

        return results

    @staticmethod
    def deduce_percentages(components_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_qty = Decimal('0')
        normalized = []

        for c in components_data:
            qty = Decimal(str(c.get('qty', 0)))
            unit = c.get('unit', 'kg')
            qty_kg = _normalize_to_kg(qty, unit)
            total_qty += qty_kg
            normalized.append({**c, 'qty_kg': float(qty_kg), 'qty': float(qty)})

        if total_qty == 0:
            return {'components': [], 'total_qty': 0}

        result_components = []
        for c in normalized:
            pct = round((Decimal(str(c['qty_kg'])) / total_qty) * Decimal('100'), 1)
            result_components.append({
                'ingredient': c.get('ingredient'),
                'sub_recipe': c.get('sub_recipe'),
                'value': float(pct),
                'unit': c.get('unit', 'kg'),
            })

        return {
            'components': result_components,
            'total_qty': float(total_qty),
        }

    @staticmethod
    def flatten_ingredients(calculated_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        flat_list = []

        for ing in calculated_data.get('ingredients', []):
            flat_list.append(ing)

        for sub in calculated_data.get('sub_recipes', []):
            flat_list.extend(RecipeCalculator.flatten_ingredients(sub))

        consolidated = {}
        for item in flat_list:
            key = (item['name'], item['unit'])
            if key in consolidated:
                consolidated[key]['qty'] += item['qty']
            else:
                consolidated[key] = dict(item)

        return list(consolidated.values())
