import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'

import 'primevue/resources/themes/saga-blue/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';
import PrimeVue from 'primevue/config';
import ToastService from 'primevue/toastservice';

import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';
import hljs from 'highlight.js';
import 'katex/dist/katex.min.css';


import ElementPlus from 'element-plus' //全局引入
import 'element-plus/dist/index.css'



const app = createApp(App);

// 监听beforeunload事件
window.addEventListener('beforeunload', () => {
  localStorage.setItem('isPageReloading', 'true')
})

window.addEventListener('load', () => {
  if (localStorage.getItem('isPageReloading') === 'true') {
    localStorage.removeItem('isPageReloading')
    router.replace('/')
  }
})

app.use(PrimeVue);
app.use(ElementPlus);
app.use(ToastService);

app.use(store);
app.use(router);



app.mount('#app');
