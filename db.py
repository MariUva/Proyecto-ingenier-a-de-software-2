import mysql.connector
import json

# Cargar la configuración de la base de datos desde el archivo JSON
with open('data/db_config.json', 'r') as config_file:
    config = json.load(config_file)

# Crear la conexión a la base de datos
def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host=config["host"],
            user=config["user"],  # Cambiado para usar "user" en lugar de "root"
            password=config["password"],  # Cambiado para usar "password" en lugar de "root"
            database=config["database"]  # Correcto, utiliza "database"
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error al conectar con la base de datos: {err}")
        return None
