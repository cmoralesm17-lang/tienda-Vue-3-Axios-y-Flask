<script setup>
// Campo de formulario reutilizable: input, select o checkbox + mensaje de error
const model = defineModel()

defineProps({
  label: { type: String, required: true },
  type: { type: String, default: 'text' },
  error: { type: String, default: '' },
  required: { type: Boolean, default: false },
  opciones: { type: Array, default: null }, // [{ value, text }] → muestra un <select>
  step: { type: String, default: undefined },
  min: { type: [String, Number], default: undefined },
})
</script>

<template>
  <label v-if="type === 'checkbox'" class="chk">
    <input type="checkbox" v-model="model" /> {{ label }}
  </label>

  <div v-else class="campo">
    <label>{{ label }}<span v-if="required" class="req"> *</span></label>

    <select v-if="opciones" v-model="model" :class="{ invalido: error }">
      <option value="" disabled>Seleccione…</option>
      <option v-for="o in opciones" :key="o.value" :value="o.value">{{ o.text }}</option>
    </select>

    <input
      v-else
      v-model="model"
      :type="type"
      :step="step"
      :min="min"
      :class="{ invalido: error }"
    />

    <small v-if="error" class="error">{{ error }}</small>
  </div>
</template>
