from models.db import execute_query


class Entrada:
    def __init__(self, row):
        self.id = row["id"]
        self.usuario_id = row["usuario_id"]
        self.fecha = row["fecha"]
        self.contenido = row["contenido"]


class EntradaModel:
    @staticmethod
    def listar_por_usuario(usuario_id):
        rows = execute_query(
            "SELECT id, usuario_id, fecha, contenido FROM entradas "
            "WHERE usuario_id = %s ORDER BY fecha DESC, id DESC",
            (usuario_id,),
        )
        return [Entrada(row) for row in rows]

    @staticmethod
    def obtener_por_id_y_usuario(entrada_id, usuario_id):
        rows = execute_query(
            "SELECT id, usuario_id, fecha, contenido FROM entradas "
            "WHERE id = %s AND usuario_id = %s",
            (entrada_id, usuario_id),
        )
        return Entrada(rows[0]) if rows else None

    @staticmethod
    def crear(usuario_id, fecha, contenido):
        return execute_query(
            "INSERT INTO entradas (usuario_id, fecha, contenido) "
            "VALUES (%s, %s, %s)",
            (usuario_id, fecha, contenido),
        )

    @staticmethod
    def actualizar(entrada_id, usuario_id, fecha, contenido):
        return execute_query(
            "UPDATE entradas SET fecha = %s, contenido = %s "
            "WHERE id = %s AND usuario_id = %s",
            (fecha, contenido, entrada_id, usuario_id),
        )

    @staticmethod
    def eliminar(entrada_id, usuario_id):
        return execute_query(
            "DELETE FROM entradas WHERE id = %s AND usuario_id = %s",
            (entrada_id, usuario_id),
        )

    @staticmethod
    def buscar(usuario_id, fecha=None, texto=None):
        query = (
            "SELECT id, usuario_id, fecha, contenido FROM entradas "
            "WHERE usuario_id = %s"
        )
        params = [usuario_id]
        if fecha:
            query += " AND fecha = %s"
            params.append(fecha)
        if texto:
            query += " AND contenido LIKE %s"
            params.append(f"%{texto}%")
        query += " ORDER BY fecha DESC, id DESC"
        rows = execute_query(query, tuple(params))
        return [Entrada(row) for row in rows]
