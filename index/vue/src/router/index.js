import { createRouter, createWebHistory } from 'vue-router'
import homeview from "../views/Home_new.vue";


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
      {
        path: '/',
        name: 'home',
        component: homeview,
      },

      {
        path: '/analyse/:userId',
        name: 'analyse',
        // route level code-splitting
        // this generates a separate chunk (About.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import('@/views/Analyse.vue'),
      },
    ],
  })

export default router