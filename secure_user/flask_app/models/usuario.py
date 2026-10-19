from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

DB = "esquema_diario"

class Usuarios:
    def __init__(self, data):
        self.id_usuario = data["id_usuario"]
        self.nombre = data["nombre"]
        self.contrasena = data["contrasena"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def guardar(cls, data):
        return connectToMySQL(DB).query_db("INSERT INTO usuarios (nombre, contrasena, created_at, updated_at) VALUES (%(nombre)s, %(contrasena)s, NOW(), NOW());", data)

    @classmethod
    def buscar_id(cls, id):
        rows = connectToMySQL(DB).query_db("SELECT * FROM usuarios WHERE id_usuario=%(id_usuario)s;", {"id_usuario": id})
        return cls(rows[0]) if rows else None

    @classmethod
    def buscar_nombre(cls, nombre):
        rows = connectToMySQL(DB).query_db("SELECT * FROM usuarios WHERE nombre=%(nombre)s;", {"nombre": nombre})
        return cls(rows[0]) if rows else None

    @staticmethod
    def validar_registro(datos):
        ok = True
        nombre = datos.get("nombre", "").strip()
        pw = datos.get("contrasena", "")
        if len(nombre) < 3 or len(nombre) > 50:
            flash("El nombre debe tener entre 3 y 50 caracteres.", "error"); ok = False
        elif Usuarios.buscar_nombre(nombre):
            flash("Ese nombre de usuario ya está registrado.", "error"); ok = False
        if len(pw) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "error"); ok = False
        if pw != datos.get("confirmar_contrasena", ""):
            flash("Las contraseñas no coinciden.", "error"); ok = False
        return ok
