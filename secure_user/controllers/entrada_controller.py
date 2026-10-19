from datetime import date, datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from controllers import login_required
from models.db import DatabaseError
from models.entrada import EntradaModel

entrada_bp = Blueprint("entrada", __name__, url_prefix="/entradas")
CONTENIDO_MAX = 5000
BUSQUEDA_MAX = 200
FECHA_MIN = date(1900, 1, 1)


def validar_entrada(fecha_texto, contenido):
    errores = []
    fecha = None
    if not fecha_texto:
        errores.append("La fecha es obligatoria.")
    else:
        try:
            fecha = datetime.strptime(fecha_texto, "%Y-%m-%d").date()
            if fecha.isoformat() != fecha_texto:
                raise ValueError
            if fecha < FECHA_MIN:
                errores.append("La fecha no puede ser anterior al año 1900.")
            elif fecha > date.today():
                errores.append("No puedes registrar entradas con fechas futuras.")
        except ValueError:
            errores.append("Introduce una fecha válida.")
    if not contenido or not contenido.strip():
        errores.append("El contenido no puede estar vacío.")
    elif len(contenido) > CONTENIDO_MAX:
        errores.append(f"El contenido no puede superar {CONTENIDO_MAX} caracteres.")
    return errores, fecha


@entrada_bp.route("/")
@login_required
def listar():
    try:
        entradas = EntradaModel.listar_por_usuario(session["usuario_id"])
    except DatabaseError:
        flash("No se pudieron cargar tus entradas. Inténtalo más tarde.", "error")
        entradas = []
    return render_template("entrada_lista.html", entradas=entradas)


@entrada_bp.route("/nueva", methods=["GET", "POST"])
@login_required
def nueva():
    fecha_texto = date.today().isoformat()
    contenido = ""
    if request.method == "POST":
        fecha_texto = request.form.get("fecha", "").strip()
        contenido = request.form.get("contenido", "")
        errores, fecha = validar_entrada(fecha_texto, contenido)
        if errores:
            for error in errores:
                flash(error, "error")
            return render_template("entrada_form.html", modo="nueva", entrada=None,
                                   fecha=fecha_texto, contenido=contenido)
        try:
            EntradaModel.crear(session["usuario_id"], fecha, contenido.strip())
        except DatabaseError:
            flash("No se pudo guardar la entrada. Inténtalo más tarde.", "error")
            return render_template("entrada_form.html", modo="nueva", entrada=None,
                                   fecha=fecha_texto, contenido=contenido)
        flash("Entrada guardada correctamente.", "success")
        return redirect(url_for("entrada.listar"))
    return render_template("entrada_form.html", modo="nueva", entrada=None,
                           fecha=fecha_texto, contenido=contenido)


@entrada_bp.route("/<int:entrada_id>")
@login_required
def detalle(entrada_id):
    try:
        entrada = EntradaModel.obtener_por_id_y_usuario(entrada_id, session["usuario_id"])
    except DatabaseError:
        flash("No se pudo cargar la entrada.", "error")
        return redirect(url_for("entrada.listar"))
    if entrada is None:
        return render_template("error.html", mensaje="La entrada no existe o no tienes permiso para verla."), 404
    return render_template("entrada_detalle.html", entrada=entrada)


@entrada_bp.route("/<int:entrada_id>/editar", methods=["GET", "POST"])
@login_required
def editar(entrada_id):
    try:
        entrada = EntradaModel.obtener_por_id_y_usuario(entrada_id, session["usuario_id"])
    except DatabaseError:
        flash("No se pudo cargar la entrada.", "error")
        return redirect(url_for("entrada.listar"))
    if entrada is None:
        return render_template("error.html", mensaje="La entrada no existe o no tienes permiso para modificarla."), 404
    fecha_texto, contenido = entrada.fecha.isoformat(), entrada.contenido
    if request.method == "POST":
        fecha_texto = request.form.get("fecha", "").strip()
        contenido = request.form.get("contenido", "")
        errores, fecha = validar_entrada(fecha_texto, contenido)
        if errores:
            for error in errores:
                flash(error, "error")
            return render_template("entrada_form.html", modo="editar", entrada=entrada,
                                   fecha=fecha_texto, contenido=contenido)
        try:
            EntradaModel.actualizar(entrada_id, session["usuario_id"], fecha, contenido.strip())
        except DatabaseError:
            flash("No se pudieron guardar los cambios. Inténtalo más tarde.", "error")
            return render_template("entrada_form.html", modo="editar", entrada=entrada,
                                   fecha=fecha_texto, contenido=contenido)
        flash("Entrada actualizada correctamente.", "success")
        return redirect(url_for("entrada.detalle", entrada_id=entrada_id))
    return render_template("entrada_form.html", modo="editar", entrada=entrada,
                           fecha=fecha_texto, contenido=contenido)


@entrada_bp.route("/<int:entrada_id>/eliminar", methods=["GET", "POST"])
@login_required
def eliminar(entrada_id):
    try:
        entrada = EntradaModel.obtener_por_id_y_usuario(entrada_id, session["usuario_id"])
    except DatabaseError:
        flash("No se pudo cargar la entrada.", "error")
        return redirect(url_for("entrada.listar"))
    if entrada is None:
        return render_template("error.html", mensaje="La entrada no existe o no tienes permiso para eliminarla."), 404
    if request.method == "POST":
        try:
            EntradaModel.eliminar(entrada_id, session["usuario_id"])
        except DatabaseError:
            flash("No se pudo eliminar la entrada. Inténtalo más tarde.", "error")
            return redirect(url_for("entrada.detalle", entrada_id=entrada_id))
        flash("Entrada eliminada correctamente.", "success")
        return redirect(url_for("entrada.listar"))
    return render_template("confirmar_eliminar.html", entrada=entrada)


@entrada_bp.route("/buscar")
@login_required
def buscar():
    fecha_texto = request.args.get("fecha", "").strip()
    texto = request.args.get("texto", "").strip()
    if len(texto) > BUSQUEDA_MAX:
        flash(f"La búsqueda no puede superar {BUSQUEDA_MAX} caracteres.", "error")
        texto = texto[:BUSQUEDA_MAX]
    fecha = None
    if fecha_texto:
        try:
            fecha = datetime.strptime(fecha_texto, "%Y-%m-%d").date()
            if fecha.isoformat() != fecha_texto:
                raise ValueError
        except ValueError:
            flash("La fecha de búsqueda no es válida.", "error")
            fecha_texto = ""
            fecha = None
    buscado = bool(fecha or texto)
    resultados = []
    if buscado:
        try:
            resultados = EntradaModel.buscar(session["usuario_id"], fecha=fecha, texto=texto or None)
        except DatabaseError:
            flash("No se pudo realizar la búsqueda. Inténtalo más tarde.", "error")
    return render_template("entrada_buscar.html", fecha=fecha_texto, texto=texto,
                           resultados=resultados, buscado=buscado)
