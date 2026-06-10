export interface Ingredient {
  id?: number;
  name: string;
  unit: 'kg' | 'g' | 'L' | 'ml' | 'pcs';
  category?: string;
  notes?: string;
}

export interface RecipeComponent {
  id?: number;
  ingredient?: number;
  ingredient_name?: string;
  sub_recipe?: number;
  sub_recipe_name?: string;
  value: number;
  unit?: string;
}

export interface Recipe {
  id?: number;
  name: string;
  instructions?: string;
  notes?: string;
  components: RecipeComponent[];
}

export interface ProductionTask {
  id?: number;
  session: number;
  recipe: number;
  recipe_name?: string;
  target_qty: number;
  target_unit: string;
  calculated_data?: any;
  status: 'PENDING' | 'IN_PROGRESS' | 'DONE';
  notes?: string;
}

export interface ProductionSession {
  id?: number;
  date: string;
  status: 'PLANNED' | 'ACTIVE' | 'COMPLETED';
  notes?: string;
  tasks: ProductionTask[];
}
