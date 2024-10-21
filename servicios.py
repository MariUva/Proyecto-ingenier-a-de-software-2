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
    def insertar_distribuidor(self, nombre, certificacion_id, contacto, calificacion_id):
        query = """
        INSERT INTO distribuidores (nombre, certificacion, contacto, calificacion)
        VALUES (%s, %s, %s, %s)
        """
        parametros = (nombre, certificacion_id, contacto, calificacion_id)
        self.cursor.execute(query, parametros)
        self.conexion.commit()

        # Obtener el ID del distribuidor recién insertado
        return self.cursor.lastrowid
    
    def insertar_calificacion(self, distribuidor_id, comentario, calificacion, fecha, cliente):
        query = """
        INSERT INTO calificacion (id_distribuidor, comentario, calificacion, fecha, cliente)
        VALUES (%s, %s, %s, %s, %s)
        """
        parametros = (distribuidor_id, comentario, calificacion, fecha, cliente)
        self.cursor.execute(query, parametros)
        self.conexion.commit()

        # Verificar que la inserción fue exitosa
        print(f"Comentario insertado para distribuidor {distribuidor_id}: {parametros}")


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

    
    def eliminar_distribuidor_logico(self, distribuidor_id):
        consulta = "UPDATE distribuidores SET eliminado = TRUE WHERE id = %s"
        self.cursor.execute(consulta, (distribuidor_id,))
        self.conexion.commit()  # Corregir a self.conexion


    def obtener_historial_distribuidores(self):
        query = """
        SELECT d.id, d.nombre, c.nombreCertificacion, d.contacto, cal.calificacion, d.eliminado
        FROM distribuidores d
        LEFT JOIN certificaciones c ON d.certificacion = c.idCertificacion
        LEFT JOIN calificacion cal ON d.calificacion = cal.idCalificacion
        """
        self.cursor.execute(query)
        distribuidores = self.cursor.fetchall()
        return distribuidores

    # Obtener todos los distribuidores
    def obtener_distribuidores(self):
        query = """
        SELECT d.id, d.nombre, c.nombreCertificacion, d.contacto, cal.calificacion
        FROM distribuidores d
        LEFT JOIN certificaciones c ON d.certificacion = c.idCertificacion
        LEFT JOIN calificacion cal ON d.calificacion = cal.idCalificacion
        WHERE d.eliminado = FALSE
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

    # Función en la clase Servicios para obtener comentarios filtrados por distribuidor
    def obtener_comentarios_distribuidor(self, distribuidor_id):
        query = """
        SELECT c.idCalificacion, c.cliente, c.calificacion, c.comentario, c.fecha
        FROM calificacion c
        WHERE c.id_distribuidor = %s
        """
        self.cursor.execute(query, (distribuidor_id,))
        comentarios = self.cursor.fetchall()

        # Añade una impresión para ver los comentarios obtenidos
        print(f"Comentarios obtenidos para el distribuidor {distribuidor_id}: {comentarios}")
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

    # Función en la clase Servicios para obtener certificaciones filtradas por distribuidor
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

    # Obtener todas las certificaciones
    def obtener_certificaciones(self):
        query = "SELECT idCertificacion, nombreCertificacion FROM certificaciones"
        self.cursor.execute(query)
        return self.cursor.fetchall()

        # Obtener todas las calificaciones
    def obtener_calificaciones(self):
        query = "SELECT idCalificacion, calificacion FROM calificacion"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insertar_entrega(self, distribuidor_id, fecha_entrega, estado_entrega):
        query = """
        INSERT INTO entregas (distribuidor_id, fecha_entrega, estado)
        VALUES (%s, %s, %s)
        """
        parametros = (distribuidor_id, fecha_entrega, estado_entrega)
        self.cursor.execute(query, parametros)
        self.conexion.commit()

    def insertar_certificacion(self, nombre, organismo_emisor, fecha_emision, fecha_expiracion, estado, puntuacion):
        query = """
        INSERT INTO certificaciones (nombreCertificacion, organismoEmisor, fechaEmision, fechaExpiracion, estado, puntuacion)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        parametros = (nombre, organismo_emisor, fecha_emision, fecha_expiracion, estado, puntuacion)
        self.cursor.execute(query, parametros)
        self.conexion.commit()
        return self.cursor.lastrowid  # Retorna el ID de la certificación recién insertada

    
    def actualizar_calificacion(self, distribuidor_id, comentario, calificacion_valor, fecha_calificacion, cliente):
        query = """
        UPDATE calificacion
        SET comentario = %s, calificacion = %s, fecha = %s, cliente = %s
        WHERE id_distribuidor = %s
        """
        parametros = (comentario, calificacion_valor, fecha_calificacion, cliente, distribuidor_id)
        self.cursor.execute(query, parametros)
        self.conexion.commit()

    def actualizar_entrega(self, distribuidor_id, fecha_entrega, estado):
        query = """
        UPDATE entregas
        SET fecha_entrega = %s, estado = %s
        WHERE distribuidor_id = %s
        """
        parametros = (fecha_entrega, estado, distribuidor_id)
        self.cursor.execute(query, parametros)
        self.conexion.commit()

    
    def obtener_distribuidores_sugeridos(self):
        query = """
        SELECT d.id, d.nombre, c.nombreCertificacion, cal.calificacion, e.estado
        FROM distribuidores d
        JOIN certificaciones c ON d.certificacion = c.idCertificacion
        JOIN calificacion cal ON d.calificacion = cal.idCalificacion
        JOIN entregas e ON d.id = e.distribuidor_id
        WHERE (cal.calificacion = 4 OR cal.calificacion = 5)
        AND (LOWER(c.nombreCertificacion) = 'calidad' OR LOWER(c.nombreCertificacion) = 'certificado textil')
        AND LOWER(e.estado) = 'completada';
        """
        self.cursor.execute(query)
        distribuidores_sugeridos = self.cursor.fetchall()
        print("Distribuidores sugeridos (desde DB):", distribuidores_sugeridos)
        return distribuidores_sugeridos



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

def buscar_distribuidores(self, criterio):
        # Lógica para buscar distribuidores según el criterio
        return [
            (1, "Distribuidor A", "Certificación A", "Contacto A", 4.5),
            # Filtrar distribuidores según el criterio
        ]
