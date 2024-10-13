from db import obtener_conexion

def verificar_distribuidor(id_distribuidor):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    query = "SELECT certificacion, reseñas FROM distribuidores WHERE id = %s"
    cursor.execute(query, (id_distribuidor,))
    
    distribuidor = cursor.fetchone()
    
    if distribuidor:
        certificacion, reseñas = distribuidor
        print(f"Distribuidor {id_distribuidor} - Certificación: {certificacion}, Reseñas: {reseñas}")
    else:
        print(f"No se encontró distribuidor con ID {id_distribuidor}")
    
    cursor.close()
    conexion.close()
