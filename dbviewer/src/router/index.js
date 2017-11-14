import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/components/Home';
import Tables from '@/components/Tables';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/tables/:id',
      name: 'Tables',
      component: Tables,
    },
  ],
});
