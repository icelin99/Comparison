import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'

import 'primevue/resources/themes/saga-blue/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';
import PrimeVue from 'primevue/config';
import ToastService from 'primevue/toastservice';

import VMdEditor from '@kangc/v-md-editor';
import '@kangc/v-md-editor/lib/style/base-editor.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';
import hljs from 'highlight.js';
import 'katex/dist/katex.min.css';

import Antd from  "ant-design-vue";
import 'ant-design-vue/dist/reset.css';


VMdEditor.use(githubTheme, {
  Hljs: hljs,
});

const app = createApp(App);

app.use(PrimeVue);
app.use(ToastService);

app.use(store);
app.use(router);

app.use(VMdEditor);
app.use(Antd);


app.mount('#app');
