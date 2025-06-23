import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

import ProjectForm from '@/views/ProjectFormView.vue';
import ProjectList from '@/views/ProjectListView.vue';
import ProjectDetails from '@/views/ProjectDetailsView.vue';
import Overview from '@/views/OverviewView.vue';
import Login from '@/views/LoginView.vue';
import Register from '@/views/RegisterView.vue';

const routes = [
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { title: 'Cadastro', requiresAuth: false }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: 'Login', requiresAuth: false },
  },
  {
    path: '/',
    name: 'Overview',
    component: Overview,
    meta: { title: 'Visão Geral', requiresAuth: true },
  },
  {
    path: '/projects',
    name: 'ProjectList',
    component: ProjectList,
    meta: { title: 'Lista de Projetos', requiresAuth: true }
  },
  {
    path: '/projects/create',
    name: 'ProjectCreate',
    component: ProjectForm,
    meta: { title: 'Cadastrar Projeto', requiresAuth: true}
  },
  {
    path: '/projects/:id',
    name: 'ProjectDetails',
    component: ProjectDetails,
    props: true,
    meta: { title: 'Detalhes do Projeto', requiresAuth: true}
  },
  {
    path: '/projects/edit/:id',
    name: 'ProjectEdit',
    component: ProjectForm,
    props: true,
    meta: { title: 'Editar Projeto', requiresAuth: true }
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  document.title = to.meta.title || 'Execução Orçamentária';
  const authStore = useAuthStore();
  const requiresAuth = to.meta.requiresAuth;
  
  if (authStore.accessToken && !authStore.user) {
    await authStore.fetchUser();
  }
  
  if (requiresAuth && !authStore.isLoggedIn) {
    next('/login');
  } else if (!requiresAuth && authStore.isLoggedIn && to.path === '/login') {
    next('/');
  } else {
    next();
  }
});

export default router;
