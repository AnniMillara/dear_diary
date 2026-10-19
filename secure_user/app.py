import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

from controllers.auth_controller import auth_bp
from controllers.entrada_controller import entrada_bp
from models.db import DatabaseError


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    if not app.secret_key:
        raise RuntimeError("Configura SECRET_KEY en el archivo .env antes de iniciar.")

    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(entrada_bp)

    @app.errorhandler(DatabaseError)
    def handle_db_error(error):
        app.logger.error("Error controlado de base de datos: %s", error)
        return render_template(
            "error.html",
            mensaje="Ha ocurrido un error interno. Inténtalo más tarde."
        ), 500

    @app.errorhandler(404)
    def handle_404(error):
        return render_template(
            "error.html", mensaje="La página que buscas no existe."
        ), 404

    @app.errorhandler(500)
    def handle_500(error):
        return render_template(
            "error.html", mensaje="Ha ocurrido un error interno."
        ), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
