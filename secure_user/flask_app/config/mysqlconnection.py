import os
import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        self.db = db

    def query_db(self, query, data=None):
        connection = pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root"),
            database=self.db,
            port=int(os.getenv("DB_PORT", 3306)),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, data)
                q = query.strip().lower()
                if q.startswith("select"):
                    return cursor.fetchall()
                if q.startswith("insert"):
                    return cursor.lastrowid
                return cursor.rowcount
        finally:
            connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)
