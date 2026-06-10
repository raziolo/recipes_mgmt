import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: () => import('../views/DashboardView.vue'),
    },
    {
      path: '/ingredients',
      name: 'Ingredients',
      component: () => import('../views/IngredientsView.vue'),
    },
    {
      path: '/recipes',
      name: 'Recipes',
      component: () => import('../views/RecipesView.vue'),
    },
    {
      path: '/production',
      name: 'Production',
      component: () => import('../views/ProductionView.vue'),
    },
  ],
});

export default router;
