import { createRouter, createWebHistory } from 'vue-router'
import SidebarView from '@/views/SidebarView.vue'
import EditorView from '@/views/EditorView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: SidebarView,
      children: [
        {
          path: '',
          name: 'home',
          component: EditorView,
        },
        {
          path: 'notes/:id',
          name: 'note-editor',
          component: EditorView,
          props: true
        }
      ],
    },
  ],
})

export default router
