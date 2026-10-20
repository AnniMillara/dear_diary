import re
from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.#]).{8,}$')

DB = "esquema_diario"

class Usuarios:
    def __init__(self, data):
        self.id_usuario = data["id_usuario"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.edad = data["edad"]
        self.email = data["email"]
        self.contrasena = data["contrasena"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # 「 ✧ CREATE ✧ 」
    # Guardar el nuevo usuario
    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO usuarios (
                nombre, 
                apellido, 
                edad,
                email, 
                contrasena, 
                created_at, 
                updated_at
            ) VALUES (
                %(nombre)s, 
                %(apellido)s, 
                %(edad)s,
                %(email)s, 
                %(contrasena)s, 
                NOW(), 
                NOW()
            );
        """
        return connectToMySQL(DB).query_db(query, data)

    # ⋆˚꩜｡ READS ｡꩜˚⋆
    # Buscar un usuario por su correo
    @classmethod
    def buscar_email(cls, email):
        query = """
            SELECT 
                * 
            FROM usuarios 
            WHERE email = %(email)s;
        """
        data = {"email": email}
        resultado = connectToMySQL(DB).query_db(query, data)
        return cls(resultado[0]) if resultado else None

    # Buscar un usuario por su ID
    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT 
                * 
            FROM usuarios 
            WHERE id_usuario = %(id_usuario)s;
        """
        data = {"id_usuario": id}
        resultado = connectToMySQL(DB).query_db(query, data)
        return cls(resultado[0]) if resultado else None

    # ─── ୨ৎ DELETE ୨ৎ ───
    # Eliminar el usuario de la base de datos
    @classmethod
    def eliminar(cls, id):
        query = """
            DELETE FROM usuarios 
            WHERE id_usuario = %(id_usuario)s;
        """
        data = {"id_usuario": id}
        return connectToMySQL(DB).query_db(query, data)

    # ⛧°. ⋆ VALIDACIONES ⋆. °⛧
    # Revisar los datos antes de registrar al usuario
    @staticmethod
    def validar_registro(datos):
        errores = []
        
        nombre = datos["nombre"].strip()
        if not nombre:
            errores.append("El nombre es obligatorio.")
        elif len(nombre) < 2 or len(nombre) > 60:
            errores.append("El nombre debe tener entre 2 y 60 caracteres.")
        elif not NAME_REGEX.match(nombre):
            errores.append("El nombre solo puede contener letras, no números ni símbolos.")

        apellido = datos["apellido"].strip()
        if not apellido:
            errores.append("El apellido es obligatorio.")
        elif len(apellido) < 2 or len(apellido) > 60:
            errores.append("El apellido debe tener entre 2 y 60 caracteres.")
        elif not NAME_REGEX.match(apellido):
            errores.append("El apellido solo puede contener letras, no números ni símbolos.")

        edad_str = datos.get("edad", "").strip()
        if not edad_str:
            errores.append("La edad es obligatoria.")
        elif not edad_str.isdigit():
            errores.append("La edad debe ser un número entero.")
        elif int(edad_str) < 18 or int(edad_str) > 120:
            errores.append("La edad debe estar entre 18 y 120 años.")

        email = datos["email"].strip()
        if not email:
            errores.append("El email es obligatorio.")
        elif len(email) > 200:
            errores.append("El email es demasiado largo.")
        elif not EMAIL_REGEX.match(email):
            errores.append("El email no tiene un formato válido.")
        elif Usuarios.buscar_email(email):
            errores.append("El email ya está registrado.")

        contrasena = datos["contrasena"]
        if not contrasena:
            errores.append("La contraseña es obligatoria.")
        elif not PASSWORD_REGEX.match(contrasena):
            errores.append("La contraseña debe tener mínimo 8 caracteres, incluyendo una mayúscula, una minúscula, un número y un carácter especial (@$!%*?&.#).")

        if contrasena != datos["confirmar_contrasena"]:
            errores.append("Las contraseñas no coinciden.")

        return errores