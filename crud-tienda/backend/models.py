from datetime import datetime
from extensions import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    nit = db.Column(db.String(20))
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(120))
    direccion = db.Column(db.String(200))
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.now)

    pedidos = db.relationship("Pedido", back_populates="cliente")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "nit": self.nit,
            "telefono": self.telefono,
            "correo": self.correo,
            "direccion": self.direccion,
        }


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    pedidos = db.relationship("Pedido", back_populates="producto")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": float(self.precio),
            "stock": self.stock,
            "activo": self.activo,
        }


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default="pendiente")
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.now)

    cliente = db.relationship("Cliente", back_populates="pedidos")
    producto = db.relationship("Producto", back_populates="pedidos")

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "cliente": self.cliente.nombre,
            "producto_id": self.producto_id,
            "producto": self.producto.nombre,
            "cantidad": self.cantidad,
            "total": float(self.total),
            "estado": self.estado,
            "fecha": self.fecha.strftime("%d/%m/%Y %H:%M"),
        }
