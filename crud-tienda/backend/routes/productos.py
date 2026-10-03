from flask import Blueprint, request, jsonify
from extensions import db
from models import Producto
from validaciones import validar_producto

bp = Blueprint("productos", __name__, url_prefix="/api/productos")


def _asignar(producto, datos):
    producto.nombre = datos["nombre"].strip()
    producto.descripcion = datos.get("descripcion") or None
    producto.precio = float(datos["precio"])
    producto.stock = int(datos["stock"])
    producto.activo = bool(datos.get("activo", True))


@bp.get("")
def listar():
    productos = Producto.query.order_by(Producto.id.desc()).all()
    return jsonify([p.to_dict() for p in productos])


@bp.get("/<int:id>")
def obtener(id):
    return jsonify(db.get_or_404(Producto, id).to_dict())


@bp.post("")
def crear():
    datos = request.get_json() or {}
    errores = validar_producto(datos)
    if errores:
        return jsonify({"errores": errores}), 400
    producto = Producto()
    _asignar(producto, datos)
    db.session.add(producto)
    db.session.commit()
    return jsonify(producto.to_dict()), 201


@bp.put("/<int:id>")
def actualizar(id):
    producto = db.get_or_404(Producto, id)
    datos = request.get_json() or {}
    errores = validar_producto(datos)
    if errores:
        return jsonify({"errores": errores}), 400
    _asignar(producto, datos)
    db.session.commit()
    return jsonify(producto.to_dict())


@bp.delete("/<int:id>")
def eliminar(id):
    producto = db.get_or_404(Producto, id)
    if producto.pedidos:
        return jsonify({"error": "No se puede eliminar: el producto tiene pedidos."}), 409
    db.session.delete(producto)
    db.session.commit()
    return jsonify({"mensaje": "Producto eliminado."})
