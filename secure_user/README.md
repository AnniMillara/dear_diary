# Querido Diario — Certificación SkillNest

Aplicación de diario personal privada desarrollada con Flask, Jinja2, MySQL y `mysql.connector`.

## Requisitos
- Python 3.11
- MySQL 8 o compatible
- Pipenv

## Instalación en PowerShell
1. Entra en la carpeta:
   ```powershell
   cd secure_user
   ```
2. Crea el archivo local de configuración:
   ```powershell
   Copy-Item .env.example .env
   ```
   Edita `.env` y configura `SECRET_KEY`, `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` y `DB_PORT`. Usa una clave secreta larga y aleatoria.
3. Crea las tablas:
   ```powershell
   Get-Content .\database\schema.sql | mysql -u root -p
   ```
   Si `mysql` no está disponible en PATH, ejecuta el archivo desde MySQL Workbench.
4. Genera el entorno y las dependencias:
   ```powershell
   pipenv install
   ```
   Este comando genera o actualiza `Pipfile.lock` según las dependencias resueltas.
5. Ejecuta la aplicación:
   ```powershell
   pipenv run python app.py
   ```
6. Abre `http://127.0.0.1:5000/`.

## Rutas principales
| Método | Ruta | Función |
|---|---|---|
| GET | `/` | Redirección inicial |
| GET/POST | `/registro` | Crear cuenta |
| GET/POST | `/login` | Iniciar sesión |
| POST | `/logout` | Cerrar sesión |
| GET | `/entradas/` | Listar entradas propias |
| GET/POST | `/entradas/nueva` | Crear entrada |
| GET | `/entradas/<id>` | Ver entrada propia |
| GET/POST | `/entradas/<id>/editar` | Editar entrada propia |
| GET/POST | `/entradas/<id>/eliminar` | Confirmar/eliminar entrada propia |
| GET | `/entradas/buscar` | Buscar entradas propias |

## Privacidad
Cada entrada guarda `usuario_id`. Las consultas de listado, detalle, edición, actualización, eliminación y búsqueda filtran por el identificador almacenado en la sesión. No se confía en un propietario enviado desde el navegador.

## Pruebas manuales recomendadas
1. Registra Ana y crea tres entradas.
2. Cierra sesión; registra Pedro y crea dos entradas.
3. Confirma que cada usuario ve solo sus entradas.
4. Como Pedro, prueba la URL de detalle y edición de una entrada de Ana. Debe responder 404 sin mostrar el contenido.
5. Prueba cancelar y confirmar la eliminación. La eliminación solo se realiza por POST.
6. Prueba fechas futuras, fechas inválidas, contenido vacío y contenido superior a 5000 caracteres.
7. Detén MySQL y comprueba que la interfaz no muestra trazas ni credenciales.

## Notas
- `.env` contiene credenciales locales y no debe subirse al repositorio.
- `Pipfile.lock` incluido es una plantilla inicial; ejecuta `pipenv install` para generar el lock real de tu entorno.
- Para un despliegue real, usa un servidor WSGI de producción y HTTPS; no uses el servidor de desarrollo de Flask.
