<script setup>
import { ref, onMounted } from 'vue'
import { useCrud } from '../composables/useCrud'
import DataTable from '../components/DataTable.vue'
import FormField from '../components/FormField.vue'
import AlertMessage from '../components/AlertMessage.vue'

function validar(d) {
  const e = {}
  if (!d.nombre?.trim()) e.nombre = 'El nombre es obligatorio.'
  if (!(Number(d.precio) > 0)) e.precio = 'El precio debe ser mayor a 0.'
  if (!Number.isInteger(Number(d.stock)) || d.stock === '' || Number(d.stock) < 0)
    e.stock = 'El stock debe ser un entero mayor o igual a 0.'
  return e
}

const { items, errores, mensaje, tipo, cargar, guardar, eliminar } = useCrud('productos', validar)

const vacio = () => ({ nombre: '', descripcion: '', precio: '', stock: 0, activo: true })
const form = ref(vacio())
const editandoId = ref(null)

const moneda = (v) => `Q ${Number(v).toFixed(2)}`
const columnas = [
  { campo: 'nombre', titulo: 'Nombre' },
  { campo: 'descripcion', titulo: 'Descripción' },
  { campo: 'precio', titulo: 'Precio', formato: moneda },
  { campo: 'stock', titulo: 'Stock' },
  { campo: 'activo', titulo: 'Estado', formato: (v) => (v ? 'Activo' : 'Inactivo') },
]

function editar(producto) {
  form.value = { ...producto }
  editandoId.value = producto.id
}
function limpiar() {
  form.value = vacio()
  editandoId.value = null
  errores.value = {}
}
async function enviar() {
  if (await guardar(form.value, editandoId.value)) limpiar()
}

onMounted(cargar)
</script>

<template>
  <h2>Productos</h2>
  <AlertMessage :texto="mensaje" :tipo="tipo" />

  <form class="formulario" @submit.prevent="enviar">
    <h3>{{ editandoId ? 'Editar producto' : 'Nuevo producto' }}</h3>
    <FormField label="Nombre" v-model="form.nombre" :error="errores.nombre" required />
    <FormField label="Descripción" v-model="form.descripcion" :error="errores.descripcion" />
    <FormField label="Precio (Q)" type="number" step="0.01" min="0" v-model="form.precio" :error="errores.precio" required />
    <FormField label="Stock" type="number" step="1" min="0" v-model="form.stock" :error="errores.stock" required />
    <FormField label="Activo" type="checkbox" v-model="form.activo" />
    <div class="form-acciones">
      <button class="btn btn-primary" type="submit">Guardar</button>
      <button class="btn" type="button" @click="limpiar">Cancelar</button>
    </div>
  </form>

  <DataTable :columnas="columnas" :filas="items" @editar="editar" @eliminar="eliminar" />
</template>
