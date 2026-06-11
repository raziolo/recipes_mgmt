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
      form: {
        name: 'Ingredient Name',
        unit: 'Base Unit',
        category: 'Category (Optional)',
        notes: 'Notes',
      },
      empty: 'No ingredients found. Start by adding one!',
    },
    recipes: {
      title: 'Recipes',
      subtitle: 'Define recipes by entering ingredient quantities.',
      createBtn: 'Create Recipe',
      empty: 'No recipes found. Create your first recipe to get started.',
      form: {
        name: 'Recipe Name',
        instructions: 'Instructions',
        components: 'Components',
        addComponent: 'Add Component',
        noComponents: 'No components yet. Add your first one!',
        ingredient: 'Ingredient',
        subRecipe: 'Sub-Recipe',
        selectIngredient: 'Select Ingredient',
        selectRecipe: 'Select Recipe',
        qty: 'Qty',
        unit: 'Unit',
        pct: '%',
        deduceBtn: 'Deduce Percentages',
        totalWeight: 'Total',
        noteQty: 'Enter quantities — percentages are computed automatically',
        tabs: {
          ingredients: 'Ingredients',
          instructions: 'Instructions',
        },
        printPreview: {
          title: 'Print Preview',
          print: 'Print',
          cancel: 'Cancel',
          components: 'Ingredients',
          instructions: 'Instructions',
        },
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
      form: {
        date: 'Production Date',
        status: 'Session Status',
        recipe: 'Select Recipe',
        targetQty: 'Target Quantity',
        taskStatus: 'Task Status',
        addTask: 'Add Recipe to Session',
      },
      actions: {
        print: 'Print Sheet',
      },
    },
    common: {
      edit: 'Edit',
      delete: 'Delete',
      save: 'Save',
      cancel: 'Cancel',
      status: {
        planned: 'Planned',
        active: 'Active',
        completed: 'Completed',
        pending: 'Pending',
        in_progress: 'In Progress',
        done: 'Done',
      }
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
      form: {
        name: 'Nome Ingrediente',
        unit: 'Unità di Misura',
        category: 'Categoria (Opzionale)',
        notes: 'Note',
      },
      empty: 'Nessun ingrediente trovato. Inizia aggiungendone uno!',
    },
    recipes: {
      title: 'Ricette',
      subtitle: 'Definisci le ricette inserendo le quantità degli ingredienti.',
      createBtn: 'Crea Ricetta',
      empty: 'Nessuna ricetta trovata. Crea la tua prima ricetta per iniziare.',
      form: {
        name: 'Nome Ricetta',
        instructions: 'Istruzioni',
        components: 'Componenti',
        addComponent: 'Aggiungi Componente',
        noComponents: 'Nessun componente. Aggiungi il primo!',
        ingredient: 'Ingrediente',
        subRecipe: 'Sotto-Ricetta',
        selectIngredient: 'Seleziona Ingrediente',
        selectRecipe: 'Seleziona Ricetta',
        qty: 'Qtà',
        unit: 'Unità',
        pct: '%',
        deduceBtn: 'Deduci Percentuali',
        totalWeight: 'Totale',
        noteQty: 'Inserisci le quantità — le percentuali sono calcolate automaticamente',
        tabs: {
          ingredients: 'Ingredienti',
          instructions: 'Istruzioni',
        },
        printPreview: {
          title: 'Anteprima Stampa',
          print: 'Stampa',
          cancel: 'Annulla',
          components: 'Ingredienti',
          instructions: 'Istruzioni',
        },
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
      form: {
        date: 'Data Produzione',
        status: 'Stato Sessione',
        recipe: 'Seleziona Ricetta',
        targetQty: 'Quantità Target',
        taskStatus: 'Stato Attività',
        addTask: 'Aggiungi Ricetta alla Sessione',
      },
      actions: {
        print: 'Stampa Scheda',
      },
    },
    common: {
      edit: 'Modifica',
      delete: 'Elimina',
      save: 'Salva',
      cancel: 'Annulla',
      status: {
        planned: 'Pianificato',
        active: 'Attivo',
        completed: 'Completato',
        pending: 'In Attesa',
        in_progress: 'In Corso',
        done: 'Fatto',
      }
    }
  }
};

const i18n = createI18n({
  legacy: false,
  locale: 'it', // Default to Italian
  fallbackLocale: 'en',
  messages,
});

export default i18n;
