# Querido Diario — SkillNest

Diario personal privado desarrollado con Flask, MySQL, PyMySQL, Flask-Bcrypt y Jinja2. Cada usuario solo puede consultar, modificar y eliminar sus propias entradas.

## Estructura

```text
secure_user/
├── server.py
├── Pipfile
├── Pipfile.lock (se genera con pipenv lock)
├── requirements.txt
├── .env.example
├── esquema.sql
└── flask_app/
    ├── __init__.py
    ├── config/mysqlconnection.py
    ├── controllers/usuarios.py
    ├── controllers/entradas.py
    ├── models/usuario.py
    ├── models/entrada.py
    ├── templates/
    └── static/css/style.css y static/js/script.js
```

## Instalación en PowerShell

1. Copia `.env.example` como `.env` y configura las credenciales de MySQL.
2. Ejecuta `mysql -u root -p < esquema.sql` desde una terminal que tenga el cliente MySQL disponible.
3. Ejecuta `pipenv install` y `pipenv shell`.
4. Ejecuta `python server.py` y abre `http://127.0.0.1:5000/`.

## Funciones

- Registro e inicio de sesión con hash de contraseñas mediante bcrypt.
- Crear, listar, ver, editar y eliminar entradas.
- Buscar por fecha y/o texto.
- Validación de fecha, contenido y contraseña.
- Consultas de entradas limitadas al usuario autenticado.
- Eliminación mediante POST con pantalla previa de confirmación.

**Importante:** `esquema.sql` elimina y vuelve a crear la base de datos `esquema_diario`. No lo ejecutes si necesitas conservar datos existentes.
