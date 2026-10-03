import { createRouter, createWebHistory } from 'vue-router'
import InicioView from '../views/InicioView.vue'
import ClientesView from '../views/ClientesView.vue'
import ProductosView from '../views/ProductosView.vue'
import PedidosView from '../views/PedidosView.vue'

const routes = [
  { path: '/', name: 'inicio', component: InicioView },
  { path: '/clientes', name: 'clientes', component: ClientesView },
  { path: '/productos', name: 'productos', component: ProductosView },
  { path: '/pedidos', name: 'pedidos', component: PedidosView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
