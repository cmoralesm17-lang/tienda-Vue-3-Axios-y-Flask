<script setup>
// Tabla reutilizable: recibe columnas y filas, emite editar / eliminar
defineProps({
  columnas: { type: Array, required: true }, // [{ campo, titulo, formato? }]
  filas: { type: Array, required: true },
})
defineEmits(['editar', 'eliminar'])
</script>

<template>
  <table class="tabla">
    <thead>
      <tr>
        <th v-for="c in columnas" :key="c.campo">{{ c.titulo }}</th>
        <th>Acciones</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="fila in filas" :key="fila.id">
        <td v-for="c in columnas" :key="c.campo">
          {{ c.formato ? c.formato(fila[c.campo]) : fila[c.campo] }}
        </td>
        <td class="acciones">
          <button class="btn btn-warning" @click="$emit('editar', fila)">Editar</button>
          <button class="btn btn-danger" @click="$emit('eliminar', fila.id)">Eliminar</button>
        </td>
      </tr>
      <tr v-if="!filas.length">
        <td :colspan="columnas.length + 1" class="vacio">No hay registros.</td>
      </tr>
    </tbody>
  </table>
</template>
