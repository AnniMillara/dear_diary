from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuarios

@app.route("/")
def inicio():
    return redirect(url_for("listado_entradas")) if "id_usuario" in session else render_template("login.html")

@app.route("/registro", methods=["POST"])
def registro():
    datos = {"nombre": request.form.get("nombre", "").strip(), "contrasena": request.form.get("contrasena", ""), "confirmar_contrasena": request.form.get("confirmar_contrasena", "")}
    if not Usuarios.validar_registro(datos): return redirect(url_for("inicio"))
    nuevo_id = Usuarios.guardar({"nombre": datos["nombre"], "contrasena": bcrypt.generate_password_hash(datos["contrasena"]).decode("utf-8")})
    session["id_usuario"] = nuevo_id; session["nombre"] = datos["nombre"]
    flash("Usuario creado correctamente.", "success")
    return redirect(url_for("listado_entradas"))

@app.route("/login", methods=["POST"])
def login():
    nombre = request.form.get("nombre", "").strip(); pw = request.form.get("contrasena", "")
    usuario = Usuarios.buscar_nombre(nombre) if nombre else None
    if not usuario or not bcrypt.check_password_hash(usuario.contrasena, pw):
        flash("Nombre o contraseña incorrectos.", "error"); return redirect(url_for("inicio"))
    session["id_usuario"] = usuario.id_usuario; session["nombre"] = usuario.nombre
    flash("Bienvenido de vuelta.", "success")
    return redirect(url_for("listado_entradas"))

@app.route("/logout")
def logout():
    session.clear(); flash("Sesión cerrada.", "success")
    return redirect(url_for("inicio"))
