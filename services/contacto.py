from db import obtener_conexion

def contactar_distribuidor(id_distribuidor):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    query = "SELECT email FROM distribuidores WHERE id = %s"
    cursor.execute(query, (id_distribuidor,))
    
    distribuidor = cursor.fetchone()
    
    if distribuidor:
        email = distribuidor[0]
        print(f"Se ha contactado al distribuidor {id_distribuidor} en el correo {email}.")
    else:
        print(f"No se encontró distribuidor con ID {id_distribuidor}")
    
    cursor.close()
    conexion.close()
