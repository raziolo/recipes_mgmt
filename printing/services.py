import datetime
from escpos.printer import Dummy, Usb, File
from typing import Dict, Any

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
        p.set(align='center', text_type='B', width=2, height=2)
        p.text(f"{(task_data.get('recipe_name') or 'UNKNOWN')}\n")
        p.set(align='center', text_type='NORMAL', width=1, height=1)
        p.text(f"Batch: {task_data.get('target_qty', 0)} {task_data.get('target_unit', '')}\n")
        p.text(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        p.text("-" * 42 + "\n")

        p.set(align='left')
        p.text("INGREDIENTS:\n")
        for ing in task_data.get('ingredients', []):
            name = ing.get('name') or 'Unknown'
            qty = float(ing.get('qty') or 0)
            unit = ing.get('unit') or ''
            qty_str = f"{qty:.3f} {unit}"
            p.text(f"{name:<30} {qty_str:>11}\n")

        if task_data.get('sub_recipes'):
            p.text("\nSUB-RECIPES:\n")
            for sub in task_data['sub_recipes']:
                s_name = sub.get('recipe_name') or 'Sub'
                s_qty = sub.get('target_qty', 0)
                s_unit = sub.get('target_unit', '')
                p.text(f"- {s_name}: {s_qty} {s_unit}\n")

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
