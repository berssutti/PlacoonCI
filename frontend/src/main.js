import { createApp } from 'vue';

import 'vuetify/styles'
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';

import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
    components,
    directives,
    icons: {
        defaultSet: 'mdi',
    },
});


createApp(App)
    .use(createPinia())
    .use(router)
    .use(vuetify)
    .mount('#app')
