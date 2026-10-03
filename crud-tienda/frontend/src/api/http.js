import axios from 'axios'

// Instancia de Axios con la dirección del backend Flask
const http = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  headers: { 'Content-Type': 'application/json' },
})

export default http
