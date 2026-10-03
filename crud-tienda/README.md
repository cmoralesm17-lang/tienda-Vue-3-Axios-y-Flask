# CRUD Tienda — Vue 3 + Axios + Flask + Flask-SQLAlchemy (PostgreSQL)

Aplicación CRUD para Windows con tres tablas relacionadas: **clientes**, **productos** y **pedidos**
(un pedido pertenece a un cliente y a un producto).

## Estructura del proyecto

```
crud-tienda/
├── backend/                  # API REST en Flask
│   ├── .env                  # cadena de conexión a PostgreSQL (no se sube al repo)
│   ├── requirements.txt      # dependencias de Python
│   ├── app.py                # crea la app, activa CORS, registra rutas y crea las tablas
│   ├── extensions.py         # objeto db = SQLAlchemy()
│   ├── models.py             # modelos Cliente, Producto y Pedido (Flask-SQLAlchemy)
│   ├── validaciones.py       # reglas de validación del servidor
│   └── routes/               # un Blueprint por tabla (GET, POST, PUT, DELETE)
│       ├── clientes.py
│       ├── productos.py
│       └── pedidos.py
└── frontend/                 # SPA en Vue 3 (Vite)
    ├── index.html
    ├── package.json
    └── src/
        ├── main.js           # monta la app y registra Vue Router
        ├── App.vue           # layout: barra de navegación + <RouterView>
        ├── router/index.js   # rutas: /, /clientes, /productos, /pedidos
        ├── api/http.js       # instancia de Axios con la URL del backend
        ├── composables/
        │   └── useCrud.js    # lógica CRUD reutilizable (listar, guardar, eliminar, errores)
        ├── components/       # componentes reutilizables
        │   ├── NavBar.vue
        │   ├── DataTable.vue # tabla genérica con botones Editar/Eliminar
        │   ├── FormField.vue # campo (input/select/checkbox) con mensaje de error
        │   └── AlertMessage.vue
        ├── views/            # una vista por módulo
        │   ├── InicioView.vue
        │   ├── ClientesView.vue
        │   ├── ProductosView.vue
        │   └── PedidosView.vue
        └── assets/main.css   # estilos
```

**Flujo:** la vista de Vue usa `useCrud` → Axios hace la petición HTTP (JSON) → Flask valida los datos,
usa los modelos de SQLAlchemy para leer/escribir en PostgreSQL → responde JSON → Vue actualiza la tabla.

**Validaciones:** se validan dos veces. En el frontend (campos obligatorios, formato de correo y teléfono,
números positivos) para dar respuesta inmediata, y en el backend (`validaciones.py`) porque es la fuente
de verdad: devuelve `400` con `{ "errores": { campo: mensaje } }` y Vue muestra cada mensaje bajo su campo.
Además: el pedido no puede superar el stock, el total se calcula en el servidor, y no se puede eliminar
un cliente o producto que tenga pedidos (`409`).

## Cómo ejecutar

Backend (PowerShell, dentro de `backend`):
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py              # http://127.0.0.1:5000
```

Frontend (otra terminal, dentro de `frontend`):
```
npm install
npm run dev                # http://localhost:5173
```

## Endpoints de la API

| Método | Ruta | Acción |
|---|---|---|
| GET | /api/{recurso} | listar |
| GET | /api/{recurso}/{id} | obtener uno |
| POST | /api/{recurso} | crear |
| PUT | /api/{recurso}/{id} | actualizar |
| DELETE | /api/{recurso}/{id} | eliminar |

`{recurso}` = `clientes`, `productos` o `pedidos`.
