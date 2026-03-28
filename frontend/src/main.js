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
                    primary: '#6366F1',
                    secondary: '#4F46E5',
                    accent: '#818CF8',
                    error: '#EF4444',
                    info: '#3B82F6',
                    success: '#10B981',
                    warning: '#F59E0B',
                    background: '#F9FAFB',
                    surface: '#FFFFFF',
                },
            },
        },
    },
    defaults: {
        VCard: {
            rounded: 'lg',
            elevation: 0,
            border: true,
        },
        VBtn: {
            rounded: 'lg',
            flat: true,
            fontWeight: '600',
            textTransform: 'none',
        },
        VTextField: {
            variant: 'outlined',
            density: 'comfortable',
            rounded: 'lg',
        },
        VSelect: {
            variant: 'outlined',
            density: 'comfortable',
            rounded: 'lg',
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
