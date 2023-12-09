import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Input from '../views/Input.vue'
import Visualize from '../views/Visualization.vue'

//creating routes for the three pages
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/input',
    name: 'Input',
    component: Input
  },
  {
    path: '/visualization',
    name: 'Visualize',
    component: Visualize
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
