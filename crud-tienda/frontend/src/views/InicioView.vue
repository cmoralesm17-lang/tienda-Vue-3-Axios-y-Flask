<template>
  <section>
    <h2>Bienvenido</h2>
    <p>Seleccione un módulo para administrar la información:</p>
    <div class="tarjetas">
      <RouterLink to="/clientes" class="tarjeta">👤 Clientes</RouterLink>
      <RouterLink to="/productos" class="tarjeta">📦 Productos</RouterLink>
      <RouterLink to="/pedidos" class="tarjeta">🧾 Pedidos</RouterLink>
    </div>
  </section>
</template>
