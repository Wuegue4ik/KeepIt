import './assets/main.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';

import Vue3Toastify, { toast } from 'vue3-toastify';
import "vue3-toastify/dist/index.css";

import App from './App.vue';
import router from './router';

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(Vue3Toastify, {
  autoClose: 5000,
  position: toast.POSITION.BOTTOM_CENTER,
  theme: toast.THEME.AUTO,
  clearOnUrlChange: false,
  pauseOnHover: true,
})

app.mount('#app');