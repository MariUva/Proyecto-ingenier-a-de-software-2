from db import conectar_db

def insertar_distribuidor(nombre, certificacion, contacto, calificacion):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        query = "INSERT INTO distribuidores (nombre, certificacion, contacto, calificacion) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nombre, certificacion, contacto, calificacion))
        conexion.commit()
        cursor.close()
        conexion.close()
        print("Distribuidor insertado con éxito")

def obtener_distribuidores():
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM distribuidores")
        distribuidores = cursor.fetchall()
        cursor.close()
        conexion.close()
        return distribuidores
