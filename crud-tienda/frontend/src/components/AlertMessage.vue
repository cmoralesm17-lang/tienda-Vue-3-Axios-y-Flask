<script setup>
defineProps({
  texto: { type: String, default: '' },
  tipo: { type: String, default: 'ok' }, // 'ok' | 'error'
})
</script>

<template>
  <div v-if="texto" :class="['alerta', tipo]">{{ texto }}</div>
</template>
