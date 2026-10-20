from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL

DB = "esquema_diario"

class Entradas:
    def __init__(self, data):
        self.id_entrada = data["id_entrada"]
        self.fecha = data["fecha"]
        self.contenido = data["contenido"]
        self.emoji = data.get("emoji", "📝")
        self.usuario_id = data["usuario_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.usuario_nombre = data.get("usuario_nombre")
        self.usuario_apellido = data.get("usuario_apellido")

    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO entradas (
                fecha, 
                contenido, 
                emoji,
                usuario_id, 
                created_at, 
                updated_at
            ) VALUES (
                %(fecha)s, 
                %(contenido)s,
                %(emoji)s,
                %(usuario_id)s,
                NOW(),
                NOW()
            );
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def ver_por_usuario(cls, usuario_id):
        query = """
            SELECT 
                e.*, 
                u.nombre AS usuario_nombre, 
                u.apellido AS usuario_apellido
            FROM entradas e
            JOIN usuarios u ON e.usuario_id = u.id_usuario
            WHERE e.usuario_id = %(usuario_id)s
            ORDER BY e.fecha DESC, e.id_entrada DESC;
        """
        resultados = connectToMySQL(DB).query_db(query, {"usuario_id": usuario_id})
        return [cls(e) for e in resultados] if resultados else []

    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT 
                e.*, 
                u.nombre AS usuario_nombre, 
                u.apellido AS usuario_apellido
            FROM entradas e
            JOIN usuarios u ON e.usuario_id = u.id_usuario
            WHERE e.id_entrada = %(id_entrada)s;
        """
        resultado = connectToMySQL(DB).query_db(query, {"id_entrada": id})
        return cls(resultado[0]) if resultado else None

    @classmethod
    def buscar_texto(cls, usuario_id, texto):
        query = """
            SELECT 
                e.id_entrada, 
                e.fecha, 
                e.contenido, 
                e.emoji,
                e.usuario_id, 
                e.created_at,
                e.updated_at,
                u.nombre AS usuario_nombre, 
                u.apellido AS usuario_apellido
            FROM entradas e
            JOIN usuarios u ON e.usuario_id = u.id_usuario
            WHERE e.usuario_id = %(usuario_id)s
              AND e.contenido LIKE %(texto)s
            ORDER BY e.fecha DESC, e.id_entrada DESC;
        """
        data = {"usuario_id": usuario_id, "texto": f"%{texto}%"}
        resultados = connectToMySQL(DB).query_db(query, data)
        return [cls(e) for e in resultados] if resultados else []

    @classmethod
    def modificar(cls, data):
        query = """
            UPDATE entradas
            SET 
                fecha = %(fecha)s, 
                contenido = %(contenido)s, 
                emoji = %(emoji)s, 
                updated_at = NOW()
            WHERE id_entrada = %(id_entrada)s 
              AND usuario_id = %(usuario_id)s;
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def eliminar(cls, id, usuario_id):
        query = """
            DELETE FROM entradas 
            WHERE id_entrada = %(id_entrada)s 
              AND usuario_id = %(usuario_id)s;
        """
        return connectToMySQL(DB).query_db(query, {"id_entrada": id, "usuario_id": usuario_id})

    @staticmethod
    def validar(datos):
        errores = []
        fecha_str = datos.get("fecha", "").strip()
        
        if not fecha_str:
            errores.append("La fecha es obligatoria.")
        else:
            try:
                if datetime.strptime(fecha_str, "%Y-%m-%d").date() > datetime.now().date():
                    errores.append("No puedes registrar entradas con fechas futuras.")
            except ValueError:
                errores.append("La fecha no tiene un formato válido.")

        contenido = datos.get("contenido", "").strip()
        if not contenido:
            errores.append("El contenido no puede estar vacío.")
        elif len(contenido) > 5000:
            errores.append("El contenido no puede superar los 5000 caracteres.")

        emoji = datos.get("emoji", "").strip()
        if len(emoji) > 10:
            errores.append("El emoji es demasiado largo (máx. 10 caracteres).")

        return errores