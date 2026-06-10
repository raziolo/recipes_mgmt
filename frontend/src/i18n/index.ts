import { createI18n } from 'vue-i18n';

const messages = {
  en: {
    nav: {
      dashboard: 'Dashboard',
      ingredients: 'Ingredients',
      recipes: 'Recipes',
      production: 'Production',
    },
    dashboard: {
      title: 'Dashboard',
      subtitle: "Overview of today's bakery production.",
      activeSessions: 'Active Sessions',
      tasksPending: 'Tasks Pending',
      completedToday: 'Completed Today',
    },
    ingredients: {
      title: 'Ingredients',
      subtitle: 'Manage raw materials and stock units.',
      addBtn: 'Add Ingredient',
      table: {
        name: 'Name',
        unit: 'Unit',
        category: 'Category',
        actions: 'Actions',
      },
      empty: 'No ingredients found. Start by adding one!',
    },
    recipes: {
      title: 'Recipes',
      subtitle: 'Define base recipes and mix percentages.',
      createBtn: 'Create Recipe',
      empty: 'No recipes found. Create your first recipe to get started.',
      methods: {
        yield: 'Yield',
        percentage: 'Percentage',
      },
      actions: {
        calculate: 'Calculate',
        edit: 'Edit',
      },
    },
    production: {
      title: 'Production',
      subtitle: 'Track and manage daily production tasks.',
      newSession: 'New Session',
      session: 'Session',
      emptyTasks: 'No tasks added to this session yet.',
      emptySessions: 'No production sessions found. Start by creating one for today!',
      actions: {
        print: 'Print Sheet',
      },
    },
    common: {
      edit: 'Edit',
      delete: 'Delete',
      save: 'Save',
      cancel: 'Cancel',
    }
  },
  it: {
    nav: {
      dashboard: 'Cruscotto',
      ingredients: 'Ingredienti',
      recipes: 'Ricette',
      production: 'Produzione',
    },
    dashboard: {
      title: 'Cruscotto',
      subtitle: 'Panoramica della produzione odierna.',
      activeSessions: 'Sessioni Attive',
      tasksPending: 'Attività In Sospeso',
      completedToday: 'Completate Oggi',
    },
    ingredients: {
      title: 'Ingredienti',
      subtitle: 'Gestisci le materie prime e le unità di misura.',
      addBtn: 'Aggiungi Ingrediente',
      table: {
        name: 'Nome',
        unit: 'Unità',
        category: 'Categoria',
        actions: 'Azioni',
      },
      empty: 'Nessun ingrediente trovato. Inizia aggiungendone uno!',
    },
    recipes: {
      title: 'Ricette',
      subtitle: 'Definisci le ricette base e le percentuali di miscelazione.',
      createBtn: 'Crea Ricetta',
      empty: 'Nessuna ricetta trovata. Crea la tua prima ricetta per iniziare.',
      methods: {
        yield: 'Resa',
        percentage: 'Percentuale',
      },
      actions: {
        calculate: 'Calcola',
        edit: 'Modifica',
      },
    },
    production: {
      title: 'Produzione',
      subtitle: 'Monitora e gestisci le attività di produzione giornaliere.',
      newSession: 'Nuova Sessione',
      session: 'Sessione',
      emptyTasks: 'Nessuna attività aggiunta a questa sessione.',
      emptySessions: 'Nessuna sessione di produzione trovata. Inizia creandone una per oggi!',
      actions: {
        print: 'Stampa Scheda',
      },
    },
    common: {
      edit: 'Modifica',
      delete: 'Elimina',
      save: 'Salva',
      cancel: 'Annulla',
    }
  }
};

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages,
});

export default i18n;
