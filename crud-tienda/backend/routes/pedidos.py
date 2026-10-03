from flask import Blueprint, request, jsonify
from extensions import db
from models import Pedido, Producto
from validaciones import validar_pedido

bp = Blueprint("pedidos", __name__, url_prefix="/api/pedidos")


def _asignar(pedido, datos):
    producto = db.session.get(Producto, int(datos["producto_id"]))
    cantidad = int(datos["cantidad"])
    pedido.cliente_id = int(datos["cliente_id"])
    pedido.producto_id = producto.id
    pedido.cantidad = cantidad
    pedido.total = producto.precio * cantidad  # el total se calcula en el servidor
    pedido.estado = datos.get("estado") or "pendiente"


@bp.get("")
def listar():
    pedidos = Pedido.query.order_by(Pedido.id.desc()).all()
    return jsonify([p.to_dict() for p in pedidos])


@bp.get("/<int:id>")
def obtener(id):
    return jsonify(db.get_or_404(Pedido, id).to_dict())


@bp.post("")
def crear():
    datos = request.get_json() or {}
    errores = validar_pedido(datos)
    if errores:
        return jsonify({"errores": errores}), 400
    pedido = Pedido()
    _asignar(pedido, datos)
    db.session.add(pedido)
    db.session.commit()
    return jsonify(pedido.to_dict()), 201


@bp.put("/<int:id>")
def actualizar(id):
    pedido = db.get_or_404(Pedido, id)
    datos = request.get_json() or {}
    errores = validar_pedido(datos)
    if errores:
        return jsonify({"errores": errores}), 400
    _asignar(pedido, datos)
    db.session.commit()
    return jsonify(pedido.to_dict())


@bp.delete("/<int:id>")
def eliminar(id):
    pedido = db.get_or_404(Pedido, id)
    db.session.delete(pedido)
    db.session.commit()
    return jsonify({"mensaje": "Pedido eliminado."})
