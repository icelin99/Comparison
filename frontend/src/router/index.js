import { createRouter, createWebHashHistory } from 'vue-router';
// import HomePage from '../App.vue';
import ImageModel from '../components/ImageModel.vue';
import MarkdownEditor from '../components/MardownEditor.vue'
import AccuracyTable from "../components/AccuracyTable.vue"
import BasePage from "../components/BasePage.vue"
import ImageVoice from "../components/ImageVoice.vue"

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
  },
  {
    path: '/voice',
    name: "ImageVoice",
    component: ImageVoice
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});


// 全局导航守卫
router.beforeEach((to, from, next) => {
  console.log("router"," from",from.path, " to",to.path);
  // if (to.path !== '/' && to.path !== '/') {
  //   next('/')
  // } else {
    next()
  // }
})

export default router;
