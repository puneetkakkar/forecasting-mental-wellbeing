import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Input from '../views/Input.vue'
import Visualize from '../views/Visualization.vue'

// We define all of our web application routes here 
// that are accessble over the web.
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

// Binding all the above routes listed above with the 
// createRouter utility provided by the vue-router
const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
