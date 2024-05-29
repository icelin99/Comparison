import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../App.vue';
import ImageModel from '../components/ImageModel.vue';
import MarkdownEditor from '../components/MardownEditor.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/image-model',
    name: 'ImageModel',
    component: ImageModel
  },
  {
    path: '/markdown',
    name: 'MarkdownEditor',
    component: MarkdownEditor
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
