import re
from extensions import db
from models import Cliente, Producto

CORREO_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
TELEFONO_RE = re.compile(r"^[0-9+\- ]{8,20}$")
ESTADOS = ("pendiente", "entregado", "cancelado")


def _texto(datos, campo):
    return str(datos.get(campo) or "").strip()


def _entero(valor):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def _decimal(valor):
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None


def validar_cliente(datos):
    errores = {}
    nombre = _texto(datos, "nombre")
    if not nombre:
        errores["nombre"] = "El nombre es obligatorio."
    elif len(nombre) > 120:
        errores["nombre"] = "Máximo 120 caracteres."

    correo = _texto(datos, "correo")
    if correo and not CORREO_RE.match(correo):
        errores["correo"] = "El correo no tiene un formato válido."

    telefono = _texto(datos, "telefono")
    if telefono and not TELEFONO_RE.match(telefono):
        errores["telefono"] = "Teléfono inválido (8 a 20 dígitos)."

    if len(_texto(datos, "nit")) > 20:
        errores["nit"] = "Máximo 20 caracteres."
    return errores


def validar_producto(datos):
    errores = {}
    if not _texto(datos, "nombre"):
        errores["nombre"] = "El nombre es obligatorio."

    precio = _decimal(datos.get("precio"))
    if precio is None or precio <= 0:
        errores["precio"] = "El precio debe ser un número mayor a 0."

    stock = _entero(datos.get("stock"))
    if stock is None or stock < 0:
        errores["stock"] = "El stock debe ser un entero mayor o igual a 0."
    return errores


def validar_pedido(datos):
    errores = {}
    cliente_id = _entero(datos.get("cliente_id"))
    if not cliente_id or not db.session.get(Cliente, cliente_id):
        errores["cliente_id"] = "Seleccione un cliente válido."

    producto_id = _entero(datos.get("producto_id"))
    producto = db.session.get(Producto, producto_id) if producto_id else None
    if not producto:
        errores["producto_id"] = "Seleccione un producto válido."
    elif not producto.activo:
        errores["producto_id"] = "El producto está inactivo."

    cantidad = _entero(datos.get("cantidad"))
    if cantidad is None or cantidad < 1:
        errores["cantidad"] = "La cantidad debe ser un entero mayor a 0."
    elif producto and cantidad > producto.stock:
        errores["cantidad"] = f"Solo hay {producto.stock} unidades disponibles."

    if (datos.get("estado") or "pendiente") not in ESTADOS:
        errores["estado"] = "Estado no válido."
    return errores
