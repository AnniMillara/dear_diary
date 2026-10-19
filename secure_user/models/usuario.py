from models.db import execute_query


class Usuario:
    def __init__(self, row):
        self.id = row["id"]
        self.nombre_usuario = row["nombre_usuario"]
        self.contrasena_hash = row["contrasena_hash"]

    @classmethod
    def obtener_por_nombre(cls, nombre_usuario):
        rows = execute_query(
            "SELECT id, nombre_usuario, contrasena_hash "
            "FROM usuarios WHERE nombre_usuario = %s",
            (nombre_usuario,),
        )
        return cls(rows[0]) if rows else None

    @classmethod
    def crear(cls, nombre_usuario, contrasena_hash):
        return execute_query(
            "INSERT INTO usuarios (nombre_usuario, contrasena_hash) "
            "VALUES (%s, %s)",
            (nombre_usuario, contrasena_hash),
        )
