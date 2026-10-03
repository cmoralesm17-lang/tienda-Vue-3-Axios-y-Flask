from flask import Blueprint, request, jsonify
from extensions import db
from models import Cliente
from validaciones import validar_cliente

bp = Blueprint("clientes", __name__, url_prefix="/api/clientes")


def _asignar(cliente, datos):
    cliente.nombre = datos["nombre"].strip()
    cliente.nit = datos.get("nit") or None
    cliente.telefono = datos.get("telefono") or None
    cliente.correo = datos.get("correo") or None
    cliente.direccion = datos.get("direccion") or None


@bp.get("")
def listar():
    clientes = Cliente.query.order_by(Cliente.id.desc()).all()
    return jsonify([c.to_dict() for c in clientes])


@bp.get("/<int:id>")
def obtener(id):
    return jsonify(db.get_or_404(Cliente, id).to_dict())


@bp.post("")
def crear():
    datos = request.get_json() or {}
    errores = validar_cliente(datos)
    if errores:
        return jsonify({"errores": errores}), 400
    cliente = Cliente()
    _asignar(cliente, datos)
    db.session.add(cliente)
    db.session.commit()
    return jsonify(cliente.to_dict()), 201


@bp.put("/<int:id>")
def actualizar(id):
    cliente = db.get_or_404(Cliente, id)
    datos = request.get_json() or {}
    errores = validar_cliente(datos)
    if errores:
        return jsonify({"errores": errores}), 400
    _asignar(cliente, datos)
    db.session.commit()
    return jsonify(cliente.to_dict())


@bp.delete("/<int:id>")
def eliminar(id):
    cliente = db.get_or_404(Cliente, id)
    if cliente.pedidos:
        return jsonify({"error": "No se puede eliminar: el cliente tiene pedidos."}), 409
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"mensaje": "Cliente eliminado."})
