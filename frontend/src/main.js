import { createApp } from 'vue';

import 'vuetify/styles'
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import App from './App.vue';
import router from './router';

import '@mdi/font/css/materialdesignicons.css'


const vuetify = createVuetify({
    components,
    directives,
    theme: {
        defaultTheme: 'light',
        themes: {
            light: {
                colors: {
                    primary: '#004e2d', // Deep Green
                    secondary: '#2563EB', // Vibrant Blue
                    error: '#EF4444',
                    info: '#3B82F6',
                    success: '#10B981',
                    warning: '#F59E0B',
                    background: '#F8F9FF', // Surface Base
                    surface: '#F8F9FF',
                    'on-surface': '#171c22', // Body Text
                    'on-background': '#171c22',
                    'surface-container-lowest': '#FFFFFF',
                    'surface-container-low': '#f0f4fd',
                    'surface-container': '#eaeef7',
                    'surface-container-high': '#e4e8f1',
                    'surface-container-highest': '#dee3eb',
                    'on-surface-variant': '#3f4941', // Labels
                },
            },
        },
    },
    defaults: {
        VCard: {
            rounded: 'xl', // 16px
            elevation: 0,
            border: false, // "No-Line" Rule
        },
        VBtn: {
            rounded: 'md', // 12px (using md for 12px based on Vuetify scale, but let's be explicit)
            flat: true,
            fontWeight: '600',
            textTransform: 'none',
        },
        VChip: {
            rounded: 'md',
        },
        VTextField: {
            variant: 'filled', // Better matches "Ghost Border" feel
            density: 'comfortable',
            rounded: 'md',
            bgColor: 'surface-container-low',
        },
        VSelect: {
            variant: 'filled',
            density: 'comfortable',
            rounded: 'md',
            bgColor: 'surface-container-low',
        },
        VDataTable: {
            density: 'comfortable',
        },
    },
    icons: {
        defaultSet: 'mdi',
    },
});


createApp(App)
    .use(router)
    .use(vuetify)
    .mount('#app')
