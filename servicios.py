import mysql.connector

class Servicios:
    def __init__(self):
        # Configuración de la conexión a la base de datos
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="sistema_compras"
        )
        self.cursor = self.conexion.cursor()

    # Insertar distribuidor
    def insertar_distribuidor(self, nombre, certificacion, contacto, calificacion):
        query = """
        INSERT INTO distribuidores (nombre, certificacion, contacto, calificacion)
        VALUES (%s, %s, %s, %s)
        """
        parametros = (nombre, certificacion, contacto, calificacion)
        self.cursor.execute(query, parametros)
        self.conexion.commit()

    # Actualizar distribuidor
    def actualizar_distribuidor(self, distribuidor_id, nombre, certificacion, contacto, calificacion):
        query = """
        UPDATE distribuidores 
        SET nombre = %s, certificacion = %s, contacto = %s, calificacion = %s
        WHERE id = %s
        """
        parametros = (nombre, certificacion, contacto, calificacion, distribuidor_id)
        self.cursor.execute(query, parametros)
        self.conexion.commit()

    # Eliminar distribuidor
    def eliminar_distribuidor(self, distribuidor_id):
        query = "DELETE FROM distribuidores WHERE id = %s"
        self.cursor.execute(query, (distribuidor_id,))
        self.conexion.commit()

    # Obtener todos los distribuidores
    def obtener_distribuidores(self):
        query = """
        SELECT d.id, d.nombre, c.nombreCertificacion, d.contacto, cal.calificacion
        FROM distribuidores d
        LEFT JOIN certificaciones c ON d.certificacion = c.idCertificacion
        LEFT JOIN calificacion cal ON d.calificacion = cal.idCalificacion
        """
        self.cursor.execute(query)
        distribuidores = self.cursor.fetchall()
        return distribuidores

    # Buscar distribuidores por nombre
    def buscar_distribuidores(self, criterio):
        query = """
        SELECT d.id, d.nombre, c.nombreCertificacion, d.contacto, cal.calificacion
        FROM distribuidores d
        LEFT JOIN certificaciones c ON d.certificacion = c.idCertificacion
        LEFT JOIN calificacion cal ON d.calificacion = cal.idCalificacion
        WHERE d.nombre LIKE %s
        """
        self.cursor.execute(query, ('%' + criterio + '%',))
        distribuidores = self.cursor.fetchall()
        return distribuidores

    # Obtener entregas por distribuidor
    def obtener_entregas_distribuidor(self, distribuidor_id):
        query = """
        SELECT e.id, d.nombre, e.fecha_entrega, e.estado
        FROM entregas e
        JOIN distribuidores d ON e.distribuidor_id = d.id
        WHERE e.distribuidor_id = %s
        """
        self.cursor.execute(query, (distribuidor_id,))
        entregas = self.cursor.fetchall()
        return entregas

    # Obtener todos los registros de entregas (sin filtro)
    def obtener_todas_las_entregas(self):
        query = """
        SELECT e.id, d.nombre, e.fecha_entrega, e.estado
        FROM entregas e
        JOIN distribuidores d ON e.distribuidor_id = d.id
        """
        self.cursor.execute(query)
        entregas = self.cursor.fetchall()
        return entregas

    # Obtener comentarios por distribuidor
    def obtener_comentarios_distribuidor(self, distribuidor_id):
        query = """
        SELECT c.idCalificacion, c.cliente, c.calificacion, c.comentario, c.fecha
        FROM calificacion c
        JOIN distribuidores d ON d.calificacion = c.idCalificacion
        WHERE d.id = %s
        """
        self.cursor.execute(query, (distribuidor_id,))
        comentarios = self.cursor.fetchall()
        return comentarios

    # Obtener todos los registros de comentarios (sin filtro)
    def obtener_todos_los_comentarios(self):
        query = """
        SELECT c.idCalificacion, c.cliente, c.calificacion, c.comentario, c.fecha
        FROM calificacion c
        """
        self.cursor.execute(query)
        comentarios = self.cursor.fetchall()
        return comentarios

    # Obtener certificaciones por distribuidor
    def obtener_certificaciones_distribuidor(self, distribuidor_id):
        query = """
        SELECT c.idCertificacion, c.nombreCertificacion, c.organismoEmisor, c.fechaEmision, c.fechaExpiracion, c.estado, c.puntuacion
        FROM certificaciones c
        JOIN distribuidores d ON d.certificacion = c.idCertificacion
        WHERE d.id = %s
        """
        self.cursor.execute(query, (distribuidor_id,))
        certificaciones = self.cursor.fetchall()
        return certificaciones

    # Obtener todos los registros de certificaciones (sin filtro)
    def obtener_todas_las_certificaciones(self):
        query = """
        SELECT c.idCertificacion, c.nombreCertificacion, c.organismoEmisor, c.fechaEmision, c.fechaExpiracion, c.estado, c.puntuacion
        FROM certificaciones c
        """
        self.cursor.execute(query)
        certificaciones = self.cursor.fetchall()
        return certificaciones
