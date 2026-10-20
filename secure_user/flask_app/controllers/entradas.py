from flask import render_template, redirect, request, session, flash, url_for, jsonify
from flask_app import app
from flask_app.models.entrada import Entradas
from flask_app.models.usuario import Usuarios

def sesion_valida():
    if "id_usuario" not in session:
        return False
    if not Usuarios.buscar_id(session["id_usuario"]):
        session.clear()
        return False
    return True

@app.route("/entradas")
def listado_entradas():
    if not sesion_valida():
        flash("Tu sesión ha expirado, por favor inicia sesión de nuevo.", "error")
        return redirect(url_for("inicio"))
    try:
        entradas = Entradas.ver_por_usuario(session["id_usuario"])
    except Exception:
        flash("No se pudieron cargar las entradas en este momento.", "error")
        entradas = []
    return render_template("entradas_lista.html", entradas=entradas)

@app.route("/entradas/nueva")
def nueva_entrada():
    if not sesion_valida():
        flash("Tu sesión ha expirado, por favor inicia sesión de nuevo.", "error")
        return redirect(url_for("inicio"))
    return render_template("entrada_form.html", entrada=None)

@app.route("/entradas/crear", methods=["POST"])
def crear_entrada():
    if not sesion_valida():
        flash("Tu sesión ha expirado, por favor inicia sesión de nuevo.", "error")
        return redirect(url_for("inicio"))
    
    datos = {
        "fecha": request.form.get("fecha", "").strip(),
        "contenido": request.form.get("contenido", "").strip(),
        "emoji": request.form.get("emoji", "").strip() or "📝",
        "usuario_id": session["id_usuario"],
    }
    
    errores = Entradas.validar(datos)
    if errores:
        for error in errores:
            flash(error, "error")
        return render_template("entrada_form.html", entrada=datos)
        
    try:
        Entradas.guardar(datos)
        flash("Entrada guardada correctamente.", "success")
        return redirect(url_for("listado_entradas"))
    except Exception:
        flash("Hubo un problema de conexión al guardar.", "error")
        return render_template("entrada_form.html", entrada=datos)

@app.route("/entradas/detalle/<int:id>")
def detalle_entrada(id):
    if not sesion_valida():
        return redirect(url_for("inicio"))
    try:
        entrada = Entradas.buscar_id(id)
        if not entrada or entrada.usuario_id != session["id_usuario"]:
            flash("Entrada no encontrada.", "error")
            return redirect(url_for("listado_entradas"))
    except Exception:
        flash("Error al buscar la entrada.", "error")
        return redirect(url_for("listado_entradas"))
    return render_template("entrada_detalle.html", entrada=entrada)

@app.route("/entradas/editar/<int:id>")
def editar_entrada(id):
    if not sesion_valida():
        return redirect(url_for("inicio"))
    try:
        entrada = Entradas.buscar_id(id)
        if not entrada or entrada.usuario_id != session["id_usuario"]:
            flash("Entrada no encontrada.", "error")
            return redirect(url_for("listado_entradas"))
    except Exception:
        flash("Error al buscar la entrada.", "error")
        return redirect(url_for("listado_entradas"))
    return render_template("entrada_form.html", entrada=entrada)

@app.route("/entradas/modificar/<int:id>", methods=["POST"])
def modificar_entrada(id):
    if not sesion_valida():
        return redirect(url_for("inicio"))
        
    datos = {
        "id_entrada": id,
        "fecha": request.form.get("fecha", "").strip(),
        "contenido": request.form.get("contenido", "").strip(),
        "emoji": request.form.get("emoji", "").strip() or "📝",
        "usuario_id": session["id_usuario"],
    }
    
    errores = Entradas.validar(datos)
    if errores:
        for error in errores:
            flash(error, "error")
        return render_template("entrada_form.html", entrada=datos)
        
    try:
        Entradas.modificar(datos)
        flash("Entrada actualizada correctamente.", "success")
        return redirect(url_for("listado_entradas"))
    except Exception:
        flash("Error al actualizar la entrada.", "error")
        return redirect(url_for("listado_entradas"))

@app.route("/entradas/confirmar_eliminar/<int:id>")
def confirmar_eliminar_entrada(id):
    if not sesion_valida():
        return redirect(url_for("inicio"))
    try:
        entrada = Entradas.buscar_id(id)
        if not entrada or entrada.usuario_id != session["id_usuario"]:
            flash("Entrada no encontrada.", "error")
            return redirect(url_for("listado_entradas"))
    except Exception:
        flash("Error al buscar la entrada.", "error")
        return redirect(url_for("listado_entradas"))
        
    return render_template("confirmar_eliminar.html",
        mensaje=f"Vas a eliminar la entrada del {entrada.fecha.strftime('%Y-%m-%d')}.",
        accion=url_for("eliminar_entrada", id=id),
        cancelar=url_for("listado_entradas"))

@app.route("/entradas/eliminar/<int:id>", methods=["POST"])
def eliminar_entrada(id):
    if not sesion_valida():
        return redirect(url_for("inicio"))
    try:
        Entradas.eliminar(id, session["id_usuario"])
        flash("Entrada eliminada.", "success")
    except Exception:
        flash("No se pudo eliminar la entrada.", "error")
    return redirect(url_for("listado_entradas"))

@app.route("/entradas/buscar_json")
def buscar_entradas_json():
    if not sesion_valida():
        return jsonify({"error": "no_autorizado"}), 401
        
    texto = request.args.get("texto", "").strip()
    try:
        if texto:
            entradas = Entradas.buscar_texto(session["id_usuario"], texto)
        else:
            entradas = Entradas.ver_por_usuario(session["id_usuario"])
    except Exception:
        return jsonify({"error": "error_db"}), 500
        
    return jsonify({
        "entradas": [{
            "id": e.id_entrada,
            "fecha_formato": e.fecha.strftime("%d/%m/%Y"),
            "emoji": e.emoji,
            "extracto": _extracto(e.contenido, 180),
        } for e in entradas]
    })

def _extracto(contenido, limite):
    plano = " ".join(contenido.split())
    return (plano[:limite].rstrip() + "…") if len(plano) > limite else plano