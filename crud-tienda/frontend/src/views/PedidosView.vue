<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCrud } from '../composables/useCrud'
import DataTable from '../components/DataTable.vue'
import FormField from '../components/FormField.vue'
import AlertMessage from '../components/AlertMessage.vue'

function validar(d) {
  const e = {}
  if (!d.cliente_id) e.cliente_id = 'Seleccione un cliente.'
  if (!d.producto_id) e.producto_id = 'Seleccione un producto.'
  if (!Number.isInteger(Number(d.cantidad)) || Number(d.cantidad) < 1)
    e.cantidad = 'La cantidad debe ser un entero mayor a 0.'
  return e
}

const { items, errores, mensaje, tipo, cargar, guardar, eliminar } = useCrud('pedidos', validar)
// Reutilizamos el mismo composable para llenar los <select>
const clientes = useCrud('clientes')
const productos = useCrud('productos')

const vacio = () => ({ cliente_id: '', producto_id: '', cantidad: 1, estado: 'pendiente' })
const form = ref(vacio())
const editandoId = ref(null)

const opcionesClientes = computed(() =>
  clientes.items.value.map((c) => ({ value: c.id, text: c.nombre })),
)
const opcionesProductos = computed(() =>
  productos.items.value
    .filter((p) => p.activo)
    .map((p) => ({ value: p.id, text: `${p.nombre} (Q ${p.precio.toFixed(2)} · stock ${p.stock})` })),
)
const opcionesEstado = [
  { value: 'pendiente', text: 'Pendiente' },
  { value: 'entregado', text: 'Entregado' },
  { value: 'cancelado', text: 'Cancelado' },
]

const totalEstimado = computed(() => {
  const p = productos.items.value.find((x) => x.id === form.value.producto_id)
  return p ? p.precio * Number(form.value.cantidad || 0) : 0
})

const moneda = (v) => `Q ${Number(v).toFixed(2)}`
const columnas = [
  { campo: 'fecha', titulo: 'Fecha' },
  { campo: 'cliente', titulo: 'Cliente' },
  { campo: 'producto', titulo: 'Producto' },
  { campo: 'cantidad', titulo: 'Cantidad' },
  { campo: 'total', titulo: 'Total', formato: moneda },
  { campo: 'estado', titulo: 'Estado' },
]

function editar(pedido) {
  form.value = {
    cliente_id: pedido.cliente_id,
    producto_id: pedido.producto_id,
    cantidad: pedido.cantidad,
    estado: pedido.estado,
  }
  editandoId.value = pedido.id
}
function limpiar() {
  form.value = vacio()
  editandoId.value = null
  errores.value = {}
}
async function enviar() {
  if (await guardar(form.value, editandoId.value)) limpiar()
}

onMounted(() => {
  cargar()
  clientes.cargar()
  productos.cargar()
})
</script>

<template>
  <h2>Pedidos</h2>
  <AlertMessage :texto="mensaje" :tipo="tipo" />

  <form class="formulario" @submit.prevent="enviar">
    <h3>{{ editandoId ? 'Editar pedido' : 'Nuevo pedido' }}</h3>
    <FormField label="Cliente" v-model="form.cliente_id" :opciones="opcionesClientes" :error="errores.cliente_id" required />
    <FormField label="Producto" v-model="form.producto_id" :opciones="opcionesProductos" :error="errores.producto_id" required />
    <FormField label="Cantidad" type="number" step="1" min="1" v-model="form.cantidad" :error="errores.cantidad" required />
    <FormField label="Estado" v-model="form.estado" :opciones="opcionesEstado" :error="errores.estado" />
    <p class="total">Total estimado: <strong>{{ moneda(totalEstimado) }}</strong></p>
    <div class="form-acciones">
      <button class="btn btn-primary" type="submit">Guardar</button>
      <button class="btn" type="button" @click="limpiar">Cancelar</button>
    </div>
  </form>

  <DataTable :columnas="columnas" :filas="items" @editar="editar" @eliminar="eliminar" />
</template>
