from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.entrada import Entradas
from flask_app.models.usuario import Usuarios

# Verificar que la sesión siga activa
def sesion_valida():
    if "id_usuario" not in session:
        return False
    if not Usuarios.buscar_id(session["id_usuario"]):
        session.clear()
        return False
    return True

# Mostrar el listado de entradas
@app.route("/entradas")
def listado_entradas():
    if not sesion_valida():
        flash("Tu sesión ha expirado.", "error")
        return redirect(url_for("inicio"))
    
    query_busqueda = request.args.get("q", "").strip()
    
    try:
        entradas = Entradas.ver_por_usuario(session["id_usuario"])
    except Exception:
        flash("No se pudieron cargar las entradas.", "error")
        entradas = []
        
    return render_template("entradas_lista.html", entradas=entradas, query=query_busqueda)

# Redirigir la búsqueda a la URL con el término
@app.route("/buscar")
def buscar_entradas_form():
    texto = request.args.get("q", "").strip()
    if texto:
        return redirect(url_for("buscar_entradas", texto=texto))
    return redirect(url_for("listado_entradas"))

# Buscar entradas por texto
@app.route("/entradas/buscar/<texto>")
def buscar_entradas(texto):
    if not sesion_valida():
        flash("Tu sesión ha expirado.", "error")
        return redirect(url_for("inicio"))
        
    try:
        entradas = Entradas.buscar_texto(session["id_usuario"], texto)
    except Exception:
        flash("Hubo un error al buscar.", "error")
        entradas = []
        
    return render_template("entradas_lista.html", entradas=entradas, query=texto)

# Mostrar formulario para nueva entrada
@app.route("/entradas/nueva")
def nueva_entrada():
    if not sesion_valida():
        return redirect(url_for("inicio"))
    return render_template("entrada_form.html", entrada=None)

# Guardar los datos de la nueva entrada
@app.route("/entradas/crear", methods=["POST"])
def crear_entrada():
    if not sesion_valida():
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
        flash("Entrada guardada.", "success")
        return redirect(url_for("listado_entradas"))
    except Exception:
        flash("Hubo un problema al guardar.", "error")
        return render_template("entrada_form.html", entrada=datos)

# Mostrar detalle de una entrada
@app.route("/entradas/detalle/<int:id>")
def detalle_entrada(id):
    if not sesion_valida():
        return redirect(url_for("inicio"))
    
    entrada = Entradas.buscar_id(id)
    if not entrada or entrada.usuario_id != session["id_usuario"]:
        flash("Entrada no encontrada.", "error")
        return redirect(url_for("listado_entradas"))
        
    return render_template("entrada_detalle.html", entrada=entrada)

# Mostrar formulario para editar entrada
@app.route("/entradas/editar/<int:id>")
def editar_entrada(id):
    if not sesion_valida():
        return redirect(url_for("inicio"))
    
    entrada = Entradas.buscar_id(id)
    if not entrada or entrada.usuario_id != session["id_usuario"]:
        flash("Entrada no encontrada.", "error")
        return redirect(url_for("listado_entradas"))
        
    return render_template("entrada_form.html", entrada=entrada)

# Actualizar los datos de la entrada
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
        flash("Entrada actualizada.", "success")
        return redirect(url_for("listado_entradas"))
    except Exception:
        flash("Error al actualizar.", "error")
        return redirect(url_for("listado_entradas"))

# Mostrar pantalla de confirmación
@app.route("/entradas/confirmar_eliminar/<int:id>")
def confirmar_eliminar_entrada(id):
    if not sesion_valida():
        return redirect(url_for("inicio"))
    
    entrada = Entradas.buscar_id(id)
    if not entrada or entrada.usuario_id != session["id_usuario"]:
        flash("Entrada no encontrada.", "error")
        return redirect(url_for("listado_entradas"))
        
    return render_template("confirmar_eliminar.html",
        mensaje=f"Vas a eliminar la entrada del {entrada.fecha.strftime('%Y-%m-%d')}.",
        accion=url_for("eliminar_entrada", id=id),
        cancelar=url_for("listado_entradas"))

# Eliminar la entrada de la base de datos
@app.route("/entradas/eliminar/<int:id>", methods=["POST"])
def eliminar_entrada(id):
    if not sesion_valida():
        return redirect(url_for("inicio"))
    try:
        Entradas.eliminar(id, session["id_usuario"])
        flash("Entrada eliminada.", "success")
    except Exception:
        flash("No se pudo eliminar.", "error")
    return redirect(url_for("listado_entradas"))