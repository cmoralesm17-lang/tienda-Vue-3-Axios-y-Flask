<script setup>
import { ref, onMounted } from 'vue'
import { useCrud } from '../composables/useCrud'
import DataTable from '../components/DataTable.vue'
import FormField from '../components/FormField.vue'
import AlertMessage from '../components/AlertMessage.vue'

function validar(d) {
  const e = {}
  if (!d.nombre?.trim()) e.nombre = 'El nombre es obligatorio.'
  if (d.correo && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.correo)) e.correo = 'Correo no válido.'
  if (d.telefono && !/^[0-9+\- ]{8,20}$/.test(d.telefono)) e.telefono = 'Teléfono inválido (8 a 20 dígitos).'
  return e
}

const { items, errores, mensaje, tipo, cargar, guardar, eliminar } = useCrud('clientes', validar)

const vacio = () => ({ nombre: '', nit: '', telefono: '', correo: '', direccion: '' })
const form = ref(vacio())
const editandoId = ref(null)

const columnas = [
  { campo: 'nombre', titulo: 'Nombre' },
  { campo: 'nit', titulo: 'NIT' },
  { campo: 'telefono', titulo: 'Teléfono' },
  { campo: 'correo', titulo: 'Correo' },
  { campo: 'direccion', titulo: 'Dirección' },
]

function editar(cliente) {
  form.value = { ...cliente }
  editandoId.value = cliente.id
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
  <h2>Clientes</h2>
  <AlertMessage :texto="mensaje" :tipo="tipo" />

  <form class="formulario" @submit.prevent="enviar">
    <h3>{{ editandoId ? 'Editar cliente' : 'Nuevo cliente' }}</h3>
    <FormField label="Nombre" v-model="form.nombre" :error="errores.nombre" required />
    <FormField label="NIT" v-model="form.nit" :error="errores.nit" />
    <FormField label="Teléfono" type="tel" v-model="form.telefono" :error="errores.telefono" />
    <FormField label="Correo" type="email" v-model="form.correo" :error="errores.correo" />
    <FormField label="Dirección" v-model="form.direccion" :error="errores.direccion" />
    <div class="form-acciones">
      <button class="btn btn-primary" type="submit">Guardar</button>
      <button class="btn" type="button" @click="limpiar">Cancelar</button>
    </div>
  </form>

  <DataTable :columnas="columnas" :filas="items" @editar="editar" @eliminar="eliminar" />
</template>
