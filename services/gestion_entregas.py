from db import conectar_db

# Función para insertar un distribuidor en la base de datos
def insertar_distribuidor(nombre, certificacion, contacto, calificacion):
    conexion = conectar_db()  # Establecer la conexión con la base de datos
    if conexion:
        try:
            cursor = conexion.cursor()
            # Consulta para insertar un nuevo distribuidor
            query = "INSERT INTO distribuidores (nombre, certificacion, contacto, calificacion) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nombre, certificacion, contacto, calificacion))
            conexion.commit()  # Confirmar los cambios en la base de datos
            print("Distribuidor insertado con éxito")
        except Exception as e:
            print(f"Error al insertar distribuidor: {e}")
        finally:
            cursor.close()
            conexion.close()  # Cerrar la conexión
    else:
        print("No se pudo establecer la conexión con la base de datos")

# Función para obtener la lista de distribuidores desde la base de datos
def obtener_distribuidores():
    conexion = conectar_db()  # Establecer la conexión con la base de datos
    if conexion:
        try:
            cursor = conexion.cursor()
            # Consulta para obtener todos los distribuidores
            cursor.execute("SELECT * FROM distribuidores")
            distribuidores = cursor.fetchall()
            return distribuidores  # Retornar los distribuidores obtenidos
        except Exception as e:
            print(f"Error al obtener distribuidores: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()  # Cerrar la conexión
    else:
        print("No se pudo establecer la conexión con la base de datos")
        return []

# Función para actualizar la información de un distribuidor
def actualizar_distribuidor(distribuidor_id, nuevo_nombre, nueva_certificacion, nuevo_contacto, nueva_calificacion):
    conexion = conectar_db()  # Conexión a la base de datos
    if conexion:
        try:
            cursor = conexion.cursor()
            # Consulta SQL para actualizar el distribuidor con la nueva información
            query = """
                UPDATE distribuidores 
                SET nombre = %s, certificacion = %s, contacto = %s, calificacion = %s 
                WHERE id = %s
            """
            cursor.execute(query, (nuevo_nombre, nueva_certificacion, nuevo_contacto, nueva_calificacion, distribuidor_id))
            conexion.commit()  # Confirmar los cambios en la base de datos
            print("Distribuidor actualizado con éxito")
        except Exception as e:
            print(f"Error al actualizar distribuidor: {e}")
        finally:
            cursor.close()
            conexion.close()  # Cerrar conexión a la base de datos
    else:
        print("No se pudo establecer la conexión con la base de datos")

# Función para eliminar un distribuidor de la base de datos
def eliminar_distribuidor(distribuidor_id):
    conexion = conectar_db()  # Conexión a la base de datos
    if conexion:
        try:
            cursor = conexion.cursor()
            # Consulta para eliminar el distribuidor
            query = "DELETE FROM distribuidores WHERE id = %s"
            cursor.execute(query, (distribuidor_id,))
            conexion.commit()  # Confirmar los cambios en la base de datos
            print("Distribuidor eliminado con éxito")
        except Exception as e:
            print(f"Error al eliminar distribuidor: {e}")
        finally:
            cursor.close()
            conexion.close()  # Cerrar la conexión
    else:
        print("No se pudo establecer la conexión con la base de datos")

# Función para buscar distribuidores por nombre, certificación o contacto
def buscar_distribuidores(criterio):
    conexion = conectar_db()  # Conexión a la base de datos
    if conexion:
        try:
            cursor = conexion.cursor()
            # Consulta para buscar distribuidores según el criterio (nombre, certificación, contacto)
            query = """
                SELECT * FROM distribuidores 
                WHERE nombre LIKE %s OR certificacion LIKE %s OR contacto LIKE %s
            """
            criterio_like = f"%{criterio}%"
            cursor.execute(query, (criterio_like, criterio_like, criterio_like))
            distribuidores = cursor.fetchall()
            return distribuidores
        except Exception as e:
            print(f"Error al buscar distribuidores: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()  # Cerrar la conexión
    else:
        print("No se pudo establecer la conexión con la base de datos")
        return []

# Función para generar un reporte de distribuidores en formato CSV
import csv
def generar_reporte():
    conexion = conectar_db()  # Establecer conexión con la base de datos
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM distribuidores")
            distribuidores = cursor.fetchall()

            # Crear y abrir el archivo CSV para escribir los datos
            with open('reporte_distribuidores.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                # Escribir la cabecera del archivo CSV
                writer.writerow(["ID", "Nombre", "Certificación", "Contacto", "Calificación"])
                
                # Escribir cada distribuidor en una fila
                for distribuidor in distribuidores:
                    writer.writerow(distribuidor)

            print("Reporte generado con éxito: reporte_distribuidores.csv")
        except Exception as e:
            print(f"Error al generar el reporte: {e}")
        finally:
            cursor.close()
            conexion.close()  # Cerrar conexión a la base de datos
    else:
        print("No se pudo establecer la conexión con la base de datos")
