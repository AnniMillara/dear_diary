from datetime import datetime
from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.entrada import Entradas

def requiere_sesion():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "error"); return False
    return True

@app.route("/entradas")
def listado_entradas():
    if not requiere_sesion(): return redirect(url_for("inicio"))
    return render_template("entradas_lista.html", entradas=Entradas.ver_por_usuario(session["id_usuario"]))

@app.route("/entradas/nueva")
def nueva_entrada():
    if not requiere_sesion(): return redirect(url_for("inicio"))
    return render_template("entrada_form.html", entrada=None)

@app.route("/entradas/crear", methods=["POST"])
def crear_entrada():
    if not requiere_sesion(): return redirect(url_for("inicio"))
    datos = {"fecha": request.form.get("fecha", "").strip(), "contenido": request.form.get("contenido", ""), "usuario_id": session["id_usuario"]}
    if not Entradas.validar(datos): return render_template("entrada_form.html", entrada=datos)
    Entradas.guardar(datos); flash("Entrada guardada correctamente.", "success")
    return redirect(url_for("listado_entradas"))

@app.route("/entradas/detalle/<int:id>")
def detalle_entrada(id):
    if not requiere_sesion(): return redirect(url_for("inicio"))
    entrada = Entradas.buscar_id_y_usuario(id, session["id_usuario"])
    if not entrada: flash("Entrada no encontrada.", "error"); return redirect(url_for("listado_entradas"))
    return render_template("entrada_detalle.html", entrada=entrada)

@app.route("/entradas/editar/<int:id>")
def editar_entrada(id):
    if not requiere_sesion(): return redirect(url_for("inicio"))
    entrada = Entradas.buscar_id_y_usuario(id, session["id_usuario"])
    if not entrada: flash("Entrada no encontrada.", "error"); return redirect(url_for("listado_entradas"))
    return render_template("entrada_form.html", entrada=entrada)

@app.route("/entradas/modificar/<int:id>", methods=["POST"])
def modificar_entrada(id):
    if not requiere_sesion(): return redirect(url_for("inicio"))
    entrada = Entradas.buscar_id_y_usuario(id, session["id_usuario"])
    if not entrada: flash("Entrada no encontrada.", "error"); return redirect(url_for("listado_entradas"))
    datos = {"id_entrada": id, "fecha": request.form.get("fecha", "").strip(), "contenido": request.form.get("contenido", ""), "usuario_id": session["id_usuario"]}
    if not Entradas.validar(datos): return render_template("entrada_form.html", entrada=datos)
    Entradas.modificar(datos); flash("Entrada actualizada correctamente.", "success")
    return redirect(url_for("detalle_entrada", id=id))

@app.route("/entradas/confirmar_eliminar/<int:id>")
def confirmar_eliminar_entrada(id):
    if not requiere_sesion(): return redirect(url_for("inicio"))
    entrada = Entradas.buscar_id_y_usuario(id, session["id_usuario"])
    if not entrada: flash("Entrada no encontrada.", "error"); return redirect(url_for("listado_entradas"))
    return render_template("confirmar_eliminar.html", mensaje=f"Vas a eliminar la entrada del {entrada.fecha.strftime('%Y-%m-%d')}. Esta acción no se puede deshacer.", accion=url_for("eliminar_entrada", id=id), cancelar=url_for("detalle_entrada", id=id))

@app.route("/entradas/eliminar/<int:id>", methods=["POST"])
def eliminar_entrada(id):
    if not requiere_sesion(): return redirect(url_for("inicio"))
    entrada = Entradas.buscar_id_y_usuario(id, session["id_usuario"])
    if not entrada: flash("Entrada no encontrada.", "error"); return redirect(url_for("listado_entradas"))
    Entradas.eliminar(id, session["id_usuario"]); flash("Entrada eliminada.", "success")
    return redirect(url_for("listado_entradas"))

@app.route("/entradas/buscar")
def buscar_entradas():
    if not requiere_sesion(): return redirect(url_for("inicio"))
    fecha = request.args.get("fecha", "").strip(); texto = request.args.get("texto", "").strip()
    if fecha:
        try: datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError: flash("El formato de fecha no es válido.", "warning"); fecha = ""
    buscado = bool(fecha or texto)
    resultados = Entradas.buscar(session["id_usuario"], fecha or None, texto or None) if buscado else []
    return render_template("entrada_buscar.html", fecha=fecha, texto=texto, resultados=resultados, buscado=buscado)
