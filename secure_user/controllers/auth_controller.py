from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from mysql.connector import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from models.db import DatabaseError
from models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)
NOMBRE_MIN = 3
NOMBRE_MAX = 50
CONTRASENA_MIN = 8
CONTRASENA_MAX = 128


@auth_bp.route("/")
def index():
    return redirect(url_for("entrada.listar") if session.get("usuario_id")
                    else url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("usuario_id"):
        return redirect(url_for("entrada.listar"))
    nombre = ""
    if request.method == "POST":
        nombre = request.form.get("nombre_usuario", "").strip()
        contrasena = request.form.get("contrasena", "")
        if not nombre or not contrasena:
            flash("Completa el nombre de usuario y la contraseña.", "error")
        else:
            try:
                usuario = Usuario.obtener_por_nombre(nombre)
            except DatabaseError:
                flash("No se pudo conectar con la base de datos. Inténtalo más tarde.", "error")
                return render_template("login.html", nombre=nombre)
            if usuario is None or not check_password_hash(usuario.contrasena_hash, contrasena):
                flash("Usuario o contraseña incorrectos.", "error")
            else:
                session.clear()
                session["usuario_id"] = usuario.id
                session["nombre_usuario"] = usuario.nombre_usuario
                flash("¡Bienvenido de vuelta!", "success")
                return redirect(url_for("entrada.listar"))
    return render_template("login.html", nombre=nombre)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if session.get("usuario_id"):
        return redirect(url_for("entrada.listar"))
    nombre = ""
    if request.method == "POST":
        nombre = request.form.get("nombre_usuario", "").strip()
        contrasena = request.form.get("contrasena", "")
        confirmar = request.form.get("confirmar_contrasena", "")
        errores = []
        if not nombre:
            errores.append("El nombre de usuario es obligatorio.")
        elif not (NOMBRE_MIN <= len(nombre) <= NOMBRE_MAX):
            errores.append(f"El nombre debe tener entre {NOMBRE_MIN} y {NOMBRE_MAX} caracteres.")
        if not contrasena:
            errores.append("La contraseña es obligatoria.")
        elif not (CONTRASENA_MIN <= len(contrasena) <= CONTRASENA_MAX):
            errores.append(f"La contraseña debe tener entre {CONTRASENA_MIN} y {CONTRASENA_MAX} caracteres.")
        if contrasena != confirmar:
            errores.append("Las contraseñas no coinciden.")
        if errores:
            for error in errores:
                flash(error, "error")
            return render_template("registro.html", nombre=nombre)
        try:
            if Usuario.obtener_por_nombre(nombre):
                flash("Ese nombre de usuario ya está registrado.", "error")
                return render_template("registro.html", nombre=nombre)
            nuevo_id = Usuario.crear(nombre, generate_password_hash(contrasena))
        except DatabaseError:
            flash("No se pudo crear la cuenta. Comprueba la base de datos e inténtalo de nuevo.", "error")
            return render_template("registro.html", nombre=nombre)
        except Exception:
            # La restricción UNIQUE protege también frente a registros simultáneos.
            flash("No se pudo crear la cuenta. Comprueba los datos e inténtalo de nuevo.", "error")
            return render_template("registro.html", nombre=nombre)
        session.clear()
        session["usuario_id"] = nuevo_id
        session["nombre_usuario"] = nombre
        flash("Cuenta creada correctamente.", "success")
        return redirect(url_for("entrada.listar"))
    return render_template("registro.html", nombre=nombre)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("auth.login"))
