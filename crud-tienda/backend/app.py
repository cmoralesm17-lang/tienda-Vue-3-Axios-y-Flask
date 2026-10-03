import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from extensions import db
from routes.clientes import bp as clientes_bp
from routes.productos import bp as productos_bp
from routes.pedidos import bp as pedidos_bp

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json.sort_keys = False

    db.init_app(app)
    CORS(app)  # permite que Vue (puerto 5173) llame a Flask (puerto 5000)

    app.register_blueprint(clientes_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(pedidos_bp)

    @app.errorhandler(404)
    def no_encontrado(e):
        return jsonify({"error": "Registro no encontrado."}), 404

    with app.app_context():
        db.create_all()  # crea las tablas clientes, productos y pedidos si no existen

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
