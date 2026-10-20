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
        self.email = data["email"]
        self.contrasena = data["contrasena"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO usuarios (
                nombre, 
                apellido, 
                email, 
                contrasena, 
                created_at, 
                updated_at
            ) VALUES (
                %(nombre)s, 
                %(apellido)s, 
                %(email)s, 
                %(contrasena)s, 
                NOW(), 
                NOW()
            );
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def buscar_email(cls, email):
        query = """
            SELECT 
                * 
            FROM usuarios 
            WHERE email = %(email)s;
        """
        resultado = connectToMySQL(DB).query_db(query, {"email": email})
        return cls(resultado[0]) if resultado else None

    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT 
                * 
            FROM usuarios 
            WHERE id_usuario = %(id_usuario)s;
        """
        resultado = connectToMySQL(DB).query_db(query, {"id_usuario": id})
        return cls(resultado[0]) if resultado else None

    @classmethod
    def eliminar(cls, id):
        query = """
            DELETE FROM usuarios 
            WHERE id_usuario = %(id_usuario)s;
        """
        return connectToMySQL(DB).query_db(query, {"id_usuario": id})

    @staticmethod
    def validar_registro(datos):
        errores = []
        
        # --- VALIDACIÓN DE NOMBRE ---
        nombre = datos["nombre"].strip()
        if not nombre:
            errores.append("El nombre es obligatorio.")
        elif len(nombre) < 2:
            errores.append("El nombre debe tener al menos 2 caracteres.")
        elif not NAME_REGEX.match(nombre):
            errores.append("El nombre solo puede contener letras, no números ni símbolos.")

        # --- VALIDACIÓN DE APELLIDO ---
        apellido = datos["apellido"].strip()
        if not apellido:
            errores.append("El apellido es obligatorio.")
        elif len(apellido) < 2:
            errores.append("El apellido debe tener al menos 2 caracteres.")
        elif not NAME_REGEX.match(apellido):
            errores.append("El apellido solo puede contener letras, no números ni símbolos.")

        # --- VALIDACIÓN DE EMAIL ---
        email = datos["email"].strip()
        if not email:
            errores.append("El email es obligatorio.")
        elif not EMAIL_REGEX.match(email):
            errores.append("El email no tiene un formato válido.")
        elif Usuarios.buscar_email(email):
            errores.append("El email ya está registrado.")

        # --- VALIDACIÓN DE CONTRASEÑA  ---
        contrasena = datos["contrasena"]
        if not contrasena:
            errores.append("La contraseña es obligatoria.")
        elif not PASSWORD_REGEX.match(contrasena):
            errores.append("La contraseña debe tener mínimo 8 caracteres, incluyendo una mayúscula, una minúscula, un número y un carácter especial (@$!%*?&.#).")

        # --- VALIDACIÓN CONFIRMACIÓN ---
        if contrasena != datos["confirmar_contrasena"]:
            errores.append("Las contraseñas no coinciden.")

        return errores