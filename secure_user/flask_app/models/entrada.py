from datetime import datetime
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

DB = "esquema_diario"
CONTENIDO_MAX = 5000

class Entradas:
    def __init__(self, data):
        self.id_entrada = data["id_entrada"]
        self.fecha = data["fecha"]
        self.contenido = data["contenido"]
        self.usuario_id = data["usuario_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def guardar(cls, data):
        return connectToMySQL(DB).query_db("INSERT INTO entradas (fecha, contenido, usuario_id, created_at, updated_at) VALUES (%(fecha)s, %(contenido)s, %(usuario_id)s, NOW(), NOW());", data)

    @classmethod
    def ver_por_usuario(cls, usuario_id):
        rows = connectToMySQL(DB).query_db("SELECT * FROM entradas WHERE usuario_id=%(usuario_id)s ORDER BY fecha DESC, id_entrada DESC;", {"usuario_id": usuario_id}) or []
        return [cls(row) for row in rows]

    @classmethod
    def buscar_id_y_usuario(cls, id_entrada, usuario_id):
        rows = connectToMySQL(DB).query_db("SELECT * FROM entradas WHERE id_entrada=%(id_entrada)s AND usuario_id=%(usuario_id)s;", {"id_entrada": id_entrada, "usuario_id": usuario_id})
        return cls(rows[0]) if rows else None

    @classmethod
    def modificar(cls, data):
        return connectToMySQL(DB).query_db("UPDATE entradas SET fecha=%(fecha)s, contenido=%(contenido)s, updated_at=NOW() WHERE id_entrada=%(id_entrada)s AND usuario_id=%(usuario_id)s;", data)

    @classmethod
    def eliminar(cls, id_entrada, usuario_id):
        return connectToMySQL(DB).query_db("DELETE FROM entradas WHERE id_entrada=%(id_entrada)s AND usuario_id=%(usuario_id)s;", {"id_entrada": id_entrada, "usuario_id": usuario_id})

    @classmethod
    def buscar(cls, usuario_id, fecha=None, texto=None):
        query = "SELECT * FROM entradas WHERE usuario_id=%(usuario_id)s"
        data = {"usuario_id": usuario_id}
        if fecha:
            query += " AND fecha=%(fecha)s"; data["fecha"] = fecha
        if texto:
            query += " AND contenido LIKE %(texto)s"; data["texto"] = f"%{texto}%"
        query += " ORDER BY fecha DESC, id_entrada DESC;"
        rows = connectToMySQL(DB).query_db(query, data) or []
        return [cls(row) for row in rows]

    @staticmethod
    def validar(datos):
        ok = True
        fecha = datos.get("fecha", "").strip()
        if not fecha:
            flash("La fecha es obligatoria.", "error"); ok = False
        else:
            try:
                if datetime.strptime(fecha, "%Y-%m-%d").date() > datetime.now().date():
                    flash("No puedes registrar entradas con fechas futuras.", "error"); ok = False
            except ValueError:
                flash("La fecha no tiene un formato válido.", "error"); ok = False
        contenido = datos.get("contenido", "")
        if not contenido.strip():
            flash("El contenido no puede estar vacío.", "error"); ok = False
        elif len(contenido.strip()) > CONTENIDO_MAX:
            flash("El contenido no puede superar los 5000 caracteres.", "error"); ok = False
        return ok
