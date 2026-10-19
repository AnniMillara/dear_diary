import logging
import os

import mysql.connector
from mysql.connector import Error


class DatabaseError(Exception):
    """Error controlado al acceder a MySQL."""


def _get_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "diario_db"),
            port=int(os.getenv("DB_PORT", "3306")),
            connection_timeout=5,
        )
    except (Error, ValueError) as error:
        logging.exception("No se pudo establecer conexión con MySQL.")
        raise DatabaseError("No se pudo conectar con la base de datos.") from error


def execute_query(query, params=None):
    connection = None
    cursor = None
    try:
        connection = _get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        normalized = query.lstrip().upper()

        if normalized.startswith("SELECT"):
            return cursor.fetchall()

        connection.commit()
        if normalized.startswith("INSERT"):
            return cursor.lastrowid
        return cursor.rowcount
    except Error as error:
        if connection is not None:
            try:
                connection.rollback()
            except Error:
                logging.exception("No se pudo revertir la transacción.")
        logging.exception("Falló una consulta de base de datos.")
        raise DatabaseError("No se pudo completar la operación.") from error
    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Error:
                logging.exception("No se pudo cerrar el cursor.")
        if connection is not None:
            try:
                if connection.is_connected():
                    connection.close()
            except Error:
                logging.exception("No se pudo cerrar la conexión.")
