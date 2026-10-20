## Querido Diario

Aplicación web de diario personal que permite a los usuarios registrar sus experiencias, guardar sus pensamientos y administrar sus entradas de forma privada. Incluye registro e inicio de sesión, perfil de usuario y un sistema CRUD para crear, visualizar, editar y eliminar entradas, además de un buscador dinámico.

Desarrollada con Python, Flask, MySQL, HTML, CSS, JavaScript y Jinja2, siguiendo una estructura MVC para organizar la lógica, las consultas a la base de datos y las vistas.

## Requisitos

- Python 3.10+
- MySQL 8+
- pip
- Pipenv

## Tecnologías

- **Python:** lógica y procesamiento de la aplicación.
- **Flask:** gestión de rutas, solicitudes y sesiones.
- **MySQL:** almacenamiento de usuarios y entradas.
- **HTML:** estructura de las páginas.
- **CSS:** diseño y estilos de la interfaz.
- **JavaScript:** interactividad y búsqueda de entradas.
- **Jinja2:** plantillas dinámicas e integración de datos en las vistas.
- **Pipenv:** administración de dependencias mediante `Pipfile` y `Pipfile.lock`.

## Funcionalidades

- Registro, inicio y cierre de sesión.
- Gestión del perfil de usuario.
- Creación, visualización, edición y eliminación de entradas.
- Búsqueda de entradas mientras se escribe.
- Registro de fechas y emojis en las entradas.
- Validación de datos y manejo de errores.
- Protección de rutas y acceso a las entradas propias de cada usuario.

## Lógica y estructura

El proyecto utiliza una organización basada en MVC:

- **Modelos:** gestionan los datos y las consultas a MySQL.
- **Controladores:** procesan las solicitudes, aplican la lógica de la aplicación y coordinan las operaciones.
- **Vistas:** muestran la información mediante HTML y plantillas Jinja2.
- **Base de datos:** relaciona los usuarios con sus entradas y almacena la información.

La aplicación utiliza sesiones para gestionar el acceso de los usuarios y validaciones para comprobar los datos antes de guardarlos o modificarlos.

## Autora

**Annerill Anabalon**  
*correo:* **annerillanabalon@liceovvh.cl**

Estudiante de programación y desarrolladora de *Querido Diario*.
Proyecto desarrollado como parte de mi aprendizaje en desarrollo web, utilizando Python, Flask, MySQL, HTML, CSS, JavaScript y Jinja2.