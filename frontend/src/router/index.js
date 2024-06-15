import { createRouter, createWebHashHistory } from 'vue-router';
// import HomePage from '../App.vue';
import ImageModel from '../components/ImageModel.vue';
import MarkdownEditor from '../components/MardownEditor.vue'
import AccuracyTable from "../components/AccuracyTable.vue"
import BasePage from "../components/BasePage.vue"

const routes = [
  // {
  //   path: '/',
  //   name: 'Home',
  //   component: HomePage
  // },
  {
    path: '/',
    name: 'Home',
    component: BasePage
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
  },
  {
    path: '/accuracy',
    name: "AccuracyTable",
    component: AccuracyTable
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

export default router;
