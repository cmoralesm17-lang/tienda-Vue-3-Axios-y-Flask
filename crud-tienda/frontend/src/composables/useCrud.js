import { ref } from 'vue'
import http from '../api/http'

/**
 * Lógica CRUD reutilizable para cualquier recurso de la API.
 * @param {string} recurso  'clientes' | 'productos' | 'pedidos'
 * @param {Function} validar  función que recibe los datos y devuelve { campo: 'mensaje' }
 */
export function useCrud(recurso, validar = () => ({})) {
  const items = ref([])
  const errores = ref({})
  const mensaje = ref('')
  const tipo = ref('ok')

  function avisar(texto, t = 'ok') {
    mensaje.value = texto
    tipo.value = t
  }

  function manejarError(e) {
    const data = e.response?.data
    if (data?.errores) {
      errores.value = data.errores
      avisar('Revise los campos marcados.', 'error')
    } else {
      avisar(data?.error || 'No se pudo conectar con el servidor.', 'error')
    }
  }

  async function cargar() {
    try {
      const { data } = await http.get(`/${recurso}`)
      items.value = data
    } catch (e) {
      manejarError(e)
    }
  }

  async function guardar(datos, id = null) {
    // 1) validación en el cliente
    errores.value = validar(datos)
    if (Object.keys(errores.value).length) {
      avisar('Revise los campos marcados.', 'error')
      return false
    }
    // 2) envío al servidor (que vuelve a validar)
    try {
      if (id) await http.put(`/${recurso}/${id}`, datos)
      else await http.post(`/${recurso}`, datos)
      avisar(id ? 'Registro actualizado correctamente.' : 'Registro creado correctamente.')
      await cargar()
      return true
    } catch (e) {
      manejarError(e)
      return false
    }
  }

  async function eliminar(id) {
    if (!confirm('¿Eliminar este registro?')) return
    try {
      await http.delete(`/${recurso}/${id}`)
      avisar('Registro eliminado.')
      await cargar()
    } catch (e) {
      manejarError(e)
    }
  }

  return { items, errores, mensaje, tipo, cargar, guardar, eliminar }
}
