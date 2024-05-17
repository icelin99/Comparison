import { createApp } from 'vue'
import App from './App.vue'
import store from './store'

import 'primevue/resources/themes/saga-blue/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';
import PrimeVue from 'primevue/config';

import VMdEditor from '@kangc/v-md-editor';
import '@kangc/v-md-editor/lib/style/base-editor.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';
import hljs from 'highlight.js';

VMdEditor.use(githubTheme, {
  Hljs: hljs,
});

const app = createApp(App);

app.use(PrimeVue);

app.use(store);

app.use(VMdEditor);



app.mount('#app');
