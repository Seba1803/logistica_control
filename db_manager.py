import sqlite3

DB_NAME = "database.db"

def conectar():
    """Conecta con la base de datos SQLite."""
    return sqlite3.connect(DB_NAME)

def crear_tablas():
    """Crea las tablas necesarias en la base de datos si no existen."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        precio REAL NOT NULL,
                        stock INTEGER NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ordenes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        producto_id INTEGER,
                        cantidad INTEGER,
                        fecha TEXT,
                        FOREIGN KEY (producto_id) REFERENCES productos (id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS envios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        orden_id INTEGER,
                        fecha_envio TEXT,
                        FOREIGN KEY (orden_id) REFERENCES ordenes (id))''')

    conn.commit()
    conn.close()

def ejecutar_query(query, params=()):
    """Ejecuta una consulta SQL en la base de datos."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def obtener_resultados(query, params=()):
    """Ejecuta una consulta SQL y devuelve los resultados."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query, params)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# Crea las tablas al importar este módulo
crear_tablas()
