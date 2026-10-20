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

    # 「 ✧ CREATE ✧ 」
    # Guardar la nueva entrada
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

    # ⋆˚꩜｡ READS ｡꩜˚⋆
    # Buscar las entradas del usuario logueado
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
        data = {"usuario_id": usuario_id}
        resultados = connectToMySQL(DB).query_db(query, data)
        
        entradas = []
        if resultados:
            for fila in resultados:
                entradas.append(cls(fila))
        return entradas

    # Buscar entradas por texto
    @classmethod
    def buscar_texto(cls, usuario_id, texto):
        query = """
            SELECT 
                e.*, 
                u.nombre AS usuario_nombre, 
                u.apellido AS usuario_apellido
            FROM entradas e
            JOIN usuarios u ON e.usuario_id = u.id_usuario
            WHERE e.usuario_id = %(usuario_id)s
            AND e.contenido LIKE %(texto)s
            ORDER BY e.fecha DESC, e.id_entrada DESC;
        """
        data = {
            "usuario_id": usuario_id,
            "texto": f"%{texto}%"
        }
        resultados = connectToMySQL(DB).query_db(query, data)
        
        entradas = []
        if resultados:
            for fila in resultados:
                entradas.append(cls(fila))
        return entradas

    # Buscar una entrada por su ID
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
        data = {"id_entrada": id}
        resultado = connectToMySQL(DB).query_db(query, data)
        return cls(resultado[0]) if resultado else None

    # ─── ୨ৎ UPDATE ୨ৎ ───
    # Modificar una entrada existente
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

    # ─── ୨ৎ DELETE ୨ৎ ───
    # Eliminar una entrada propia
    @classmethod
    def eliminar(cls, id, usuario_id):
        query = """
            DELETE FROM entradas 
            WHERE id_entrada = %(id_entrada)s 
            AND usuario_id = %(usuario_id)s;
        """
        data = {
            "id_entrada": id,
            "usuario_id": usuario_id
        }
        return connectToMySQL(DB).query_db(query, data)

    # ⛧°. ⋆ VALIDACIONES ⋆. °⛧
    # Revisar los datos antes de guardar la entrada
    @staticmethod
    def validar(datos):
        errores = []
        
        if not datos.get("fecha", "").strip():
            errores.append("La fecha es obligatoria.")
        else:
            try:
                fecha_ingresada = datetime.strptime(datos["fecha"], "%Y-%m-%d").date()
                if fecha_ingresada > datetime.now().date():
                    errores.append("No puedes registrar entradas con fechas futuras.")
            except ValueError:
                errores.append("La fecha no tiene un formato válido.")

        if not datos.get("contenido", "").strip():
            errores.append("El contenido no puede estar vacío.")
        elif len(datos["contenido"]) > 5000:
            errores.append("El contenido no puede superar los 5000 caracteres.")

        if len(datos.get("emoji", "")) > 10:
            errores.append("El emoji es demasiado largo.")

        return errores