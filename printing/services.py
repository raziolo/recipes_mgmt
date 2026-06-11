import datetime
from typing import Dict, Any, Tuple
from escpos.printer import Dummy, Usb, File


def _normalize_display_qty(qty_kg: float, unit: str) -> Tuple[float, str]:
    u = unit.lower()
    if u in ('g', 'gr'):
        return round(qty_kg * 1000, 2), 'g'
    if u == 'kg':
        if qty_kg < 1:
            return round(qty_kg * 1000, 2), 'g'
        return round(qty_kg, 3), 'kg'
    if u == 'l':
        if qty_kg < 1:
            return round(qty_kg * 1000, 2), 'ml'
        return round(qty_kg, 3), 'L'
    if u == 'ml':
        return round(qty_kg * 1000, 2), 'ml'
    return round(qty_kg, 3), unit


class ProductionSheetPrinter:
    def __init__(self, printer_type='dummy', **kwargs):
        """
        printer_type: 'usb', 'file', or 'dummy'
        """
        if printer_type == 'usb':
            # Example: vendor_id=0x04b8, product_id=0x0202
            self.p = Usb(kwargs.get('vendor_id'), kwargs.get('product_id'))
        elif printer_type == 'file':
            self.p = File(kwargs.get('filename', 'print_out.bin'))
        else:
            self.p = Dummy()

    def print_task(self, task_data: Dict[str, Any]):
        p = self.p
        p.set(align='center', bold=True, double_width=True, double_height=True)
        p.text(f"{(task_data.get('recipe_name') or 'UNKNOWN')}\n")
        p.set(align='center')
        p.text(f"Batch: {task_data.get('target_qty', 0)} {task_data.get('target_unit', '')}\n")
        p.text(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        p.text("-" * 42 + "\n")

        p.set(align='left')
        p.text("INGREDIENTS:\n")
        for ing in task_data.get('ingredients', []):
            name = ing.get('name') or 'Unknown'
            qty_raw = float(ing.get('qty') or 0)
            unit_raw = ing.get('unit') or ''
            norm_qty, norm_unit = _normalize_display_qty(qty_raw, unit_raw)
            qty_str = f"{norm_qty:.{2 if norm_unit in ('g','ml') else 3}f} {norm_unit}"
            p.text(f"{name:<30} {qty_str:>11}\n")

        if task_data.get('sub_recipes'):
            p.text("\nSUB-RECIPES:\n")
            for sub in task_data['sub_recipes']:
                s_name = sub.get('recipe_name') or 'Sub'
                s_qty_raw = sub.get('target_qty', 0)
                s_unit_raw = sub.get('target_unit', '')
                sn_qty, sn_unit = _normalize_display_qty(s_qty_raw, s_unit_raw)
                p.text(f"- {s_name}: {sn_qty:.{2 if sn_unit in ('g','ml') else 3}f} {sn_unit}\n")

        p.text("-" * 42 + "\n")
        p.text("INSTRUCTIONS:\n")
        instr = task_data.get('instructions') or 'See master recipe.'
        p.text(str(instr) + "\n")
        
        p.text("\n\n")
        p.cut()

    def get_output(self):
        if isinstance(self.p, Dummy):
            return self.p.output
        return None
