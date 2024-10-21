import tkinter as tk
from tkinter import ttk, messagebox
from servicios import Servicios
from tkcalendar import DateEntry
from fpdf import FPDF

# Inicializar la clase Servicios para conectar a la base de datos
servicios = Servicios()

# Lista global para almacenar los distribuidores seleccionados
distribuidores_seleccionados = []

def iniciar_gui():
    root = tk.Tk()
    root.title("Gestión de Distribuidores")
    root.geometry("1024x500")

    # Centrar la ventana principal
    centrar_ventana(root)

    # Crear un Notebook para las pestañas
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    # Pestaña de Distribuidores
    frame_distribuidores = tk.Frame(notebook)
    notebook.add(frame_distribuidores, text="Distribuidores")

    # Pestaña de Entregas
    frame_entregas = tk.Frame(notebook)
    notebook.add(frame_entregas, text="Gestión de entregas")

    # Pestaña de Distribuidores Seleccionados
    frame_distribuidores_seleccionados = tk.Frame(notebook)
    notebook.add(frame_distribuidores_seleccionados, text="Distribuidores Seleccionados")


    # ------------------------- PESTAÑA DISTRIBUIDORES -------------------------
    # Título en la pestaña de Distribuidores
    titulo = tk.Label(frame_distribuidores, text="Gestión de Distribuidores", font=("Arial", 16))
    titulo.pack(pady=10)

    # Crear frame para la tabla
    frame_tabla = tk.Frame(frame_distribuidores)
    frame_tabla.pack(pady=10)

    # Encabezados de la tabla de distribuidores
    columnas = ("ID", "Nombre", "Certificación", "Contacto", "Calificación")
    global tabla_distribuidores
    tabla_distribuidores = ttk.Treeview(frame_tabla, columns=columnas, show='headings')

    # Definir encabezados
    for columna in columnas:
        tabla_distribuidores.heading(columna, text=columna)

    # Ancho de columnas
    tabla_distribuidores.column("ID", width=50)
    tabla_distribuidores.column("Nombre", width=150)
    tabla_distribuidores.column("Certificación", width=150)
    tabla_distribuidores.column("Contacto", width=150)
    tabla_distribuidores.column("Calificación", width=100)

    # Insertar datos en la tabla
    mostrar_distribuidores()
    tabla_distribuidores.pack()

    # Crear frame para la búsqueda
    frame_busqueda = tk.Frame(frame_distribuidores)
    frame_busqueda.pack(pady=10)

    global entry_busqueda  # Hacer global la entrada de búsqueda
    tk.Label(frame_busqueda, text="Buscar Distribuidor por Nombre").grid(row=0, column=0)
    entry_busqueda = tk.Entry(frame_busqueda)
    entry_busqueda.grid(row=0, column=1, padx=10)

    btn_buscar = tk.Button(frame_busqueda, text="Buscar", command=buscar_distribuidor, bg="yellow", fg="black")
    btn_buscar.grid(row=0, column=2)

    # Crear frame para los botones de CRUD y seleccionar distribuidor
    frame_botones = tk.Frame(frame_distribuidores)
    frame_botones.pack(pady=10)

    # Botones CRUD con colores
    btn_crear = tk.Button(frame_botones, text="Crear Distribuidor", command=crear_distribuidor, bg="green", fg="white")
    btn_crear.grid(row=0, column=0, padx=10)

    btn_modificar = tk.Button(frame_botones, text="Modificar Distribuidor", command=modificar_distribuidor, bg="blue", fg="white")
    btn_modificar.grid(row=0, column=1, padx=10)

    btn_eliminar = tk.Button(frame_botones, text="Eliminar Distribuidor", command=eliminar_distribuidor_ui, bg="red", fg="white")
    btn_eliminar.grid(row=0, column=2, padx=10)

    # Botón para seleccionar distribuidor
    btn_seleccionar = tk.Button(frame_botones, text="Seleccionar Distribuidor", command=seleccionar_distribuidor, bg="orange", fg="white")
    btn_seleccionar.grid(row=0, column=3, padx=10)

    # ------------------------- PESTAÑA DISTRIBUIDORES SELECCIONADOS -------------------------
    # Título en la pestaña de Distribuidores Seleccionados
    titulo_seleccionados = tk.Label(frame_distribuidores_seleccionados, text="Distribuidores Seleccionados", font=("Arial", 16))
    titulo_seleccionados.pack(pady=10)

    # Crear frame para la tabla de distribuidores seleccionados
    frame_tabla_seleccionados = tk.Frame(frame_distribuidores_seleccionados)
    frame_tabla_seleccionados.pack(pady=10)

    # Encabezados de la tabla de distribuidores seleccionados
    columnas_seleccionados = ("ID", "Nombre", "Certificación", "Contacto", "Calificación")
    global tabla_distribuidores_seleccionados
    tabla_distribuidores_seleccionados = ttk.Treeview(frame_tabla_seleccionados, columns=columnas_seleccionados, show='headings')

    # Definir encabezados para la tabla de distribuidores seleccionados
    for columna in columnas_seleccionados:
        tabla_distribuidores_seleccionados.heading(columna, text=columna)

    # Ancho de columnas de la tabla de seleccionados
    tabla_distribuidores_seleccionados.column("ID", width=50)
    tabla_distribuidores_seleccionados.column("Nombre", width=150)
    tabla_distribuidores_seleccionados.column("Certificación", width=150)
    tabla_distribuidores_seleccionados.column("Contacto", width=150)
    tabla_distribuidores_seleccionados.column("Calificación", width=100)

    tabla_distribuidores_seleccionados.pack()

    # Botón para generar reporte en PDF
    btn_generar_pdf = tk.Button(frame_distribuidores_seleccionados, text="Generar Reporte PDF", command=generar_reporte_pdf, bg="green", fg="white")
    btn_generar_pdf.pack(pady=10)

    # ------------------------- PESTAÑA ENTREGAS -------------------------

    # Título en la pestaña de Entregas
    titulo_entregas = tk.Label(frame_entregas, text="Entregas por Distribuidor", font=("Arial", 16))
    titulo_entregas.pack(pady=10)

    # Crear frame para la tabla de entregas
    frame_tabla_entregas = tk.Frame(frame_entregas)
    frame_tabla_entregas.pack(pady=10)

    # Encabezados de la tabla de entregas
    columnas_entregas = ("ID Entrega", "Distribuidor", "Fecha Entrega", "Estado")
    global tabla_entregas
    tabla_entregas = ttk.Treeview(frame_tabla_entregas, columns=columnas_entregas, show='headings')

    # Definir encabezados
    for columna in columnas_entregas:
        tabla_entregas.heading(columna, text=columna)

    # Ancho de columnas de entregas
    tabla_entregas.column("ID Entrega", width=100)
    tabla_entregas.column("Distribuidor", width=150)
    tabla_entregas.column("Fecha Entrega", width=150)
    tabla_entregas.column("Estado", width=100)

    tabla_entregas.pack()

     # Mostrar las entregas al cargar la pestaña
    mostrar_entregas()
    tabla_entregas.pack()


    # Botón para cargar entregas de un distribuidor seleccionado
    btn_cargar_entregas = tk.Button(frame_entregas, text="Cargar Entregas", command=cargar_entregas_distribuidor, bg="yellow", fg="black")
    btn_cargar_entregas.pack(pady=10)

 # ------------------------- PESTAÑA COMENTARIOS -------------------------
    
    # Definir la pestaña de Comentarios antes de usarla
    frame_comentarios = tk.Frame(notebook)
    notebook.add(frame_comentarios, text="Calificaciones")

    # Título en la pestaña de Comentarios
    titulo_comentarios = tk.Label(frame_comentarios, text="Calificaciones por Distribuidor", font=("Arial", 16))
    titulo_comentarios.pack(pady=10)

    # Crear frame para la tabla de comentarios
    frame_tabla_comentarios = tk.Frame(frame_comentarios)
    frame_tabla_comentarios.pack(pady=10)

    # Encabezados de la tabla de comentarios
    columnas_comentarios = ("ID Comentario", "Cliente", "Calificación", "Comentario", "Fecha")
    global tabla_comentarios
    tabla_comentarios = ttk.Treeview(frame_tabla_comentarios, columns=columnas_comentarios, show='headings')

    # Definir encabezados
    for columna in columnas_comentarios:
        tabla_comentarios.heading(columna, text=columna)

    # Ancho de columnas de comentarios
    tabla_comentarios.column("ID Comentario", width=100)
    tabla_comentarios.column("Cliente", width=150)
    tabla_comentarios.column("Calificación", width=100)
    tabla_comentarios.column("Comentario", width=300)
    tabla_comentarios.column("Fecha", width=150)

    # Mostrar los comentarios al cargar la pestaña
    mostrar_comentarios()
    tabla_comentarios.pack()

    # Botón para cargar comentarios de un distribuidor seleccionado
    btn_cargar_comentarios = tk.Button(frame_comentarios, text="Cargar Comentarios", command=cargar_comentarios_distribuidor, bg="yellow", fg="black")
    btn_cargar_comentarios.pack(pady=10)



# ------------------------- PESTAÑA VALIDAR CERTIFICACIONES -------------------------
    
    # Definir la pestaña de Certificaciones
    frame_certificaciones = tk.Frame(notebook)
    notebook.add(frame_certificaciones, text="Validar Certificaciones")

    # Título en la pestaña de Certificaciones
    titulo_certificaciones = tk.Label(frame_certificaciones, text="Certificaciones por Distribuidor", font=("Arial", 16))
    titulo_certificaciones.pack(pady=10)

    # Crear frame para la tabla de certificaciones
    frame_tabla_certificaciones = tk.Frame(frame_certificaciones)
    frame_tabla_certificaciones.pack(pady=10)

    # Encabezados de la tabla de certificaciones
    columnas_certificaciones = ("ID Certificación", "Nombre", "Organismo Emisor", "Fecha Emisión", "Fecha Expiración", "Estado", "Puntuación")
    global tabla_certificaciones
    tabla_certificaciones = ttk.Treeview(frame_tabla_certificaciones, columns=columnas_certificaciones, show='headings')

    # Definir encabezados
    for columna in columnas_certificaciones:
        tabla_certificaciones.heading(columna, text=columna)

    # Ancho de columnas de certificaciones
    tabla_certificaciones.column("ID Certificación", width=100)
    tabla_certificaciones.column("Nombre", width=150)
    tabla_certificaciones.column("Organismo Emisor", width=150)
    tabla_certificaciones.column("Fecha Emisión", width=150)
    tabla_certificaciones.column("Fecha Expiración", width=150)
    tabla_certificaciones.column("Estado", width=100)
    tabla_certificaciones.column("Puntuación", width=100)

    tabla_certificaciones.pack()

     # Mostrar las certificaciones al cargar la pestaña
    mostrar_certificaciones()
    tabla_certificaciones.pack()

    # Botón para cargar certificaciones de un distribuidor seleccionado
    btn_cargar_certificaciones = tk.Button(frame_certificaciones, text="Cargar Certificaciones", command=cargar_certificaciones_distribuidor, bg="yellow", fg="black")
    btn_cargar_certificaciones.pack(pady=10)

# ----------------------------- DISTRIBUIDORES SUGERIDOS -----------------------------
    # Crear frame para la pestaña de distribuidores sugeridos
    frame_sugeridos = tk.Frame(notebook)
    notebook.add(frame_sugeridos, text="Distribuidores Sugeridos")

    # Título para la pestaña de distribuidores sugeridos
    titulo_sugeridos = tk.Label(frame_sugeridos, text="Distribuidores Sugeridos", font=("Arial", 16))
    titulo_sugeridos.pack(pady=10)

    # Crear frame para la tabla de distribuidores sugeridos
    frame_tabla_sugeridos = tk.Frame(frame_sugeridos)
    frame_tabla_sugeridos.pack(pady=10)

    # Encabezados de la tabla de distribuidores sugeridos
    columnas_sugeridos = ("ID", "Nombre", "Certificación", "Calificación", "Estado de Entrega")
    global tabla_sugeridos_distribuidores
    tabla_sugeridos_distribuidores = ttk.Treeview(frame_tabla_sugeridos, columns=columnas_sugeridos, show='headings')

    # Definir encabezados
    for columna in columnas_sugeridos:
        tabla_sugeridos_distribuidores.heading(columna, text=columna)

    # Ancho de columnas
    tabla_sugeridos_distribuidores.column("ID", width=50)
    tabla_sugeridos_distribuidores.column("Nombre", width=150)
    tabla_sugeridos_distribuidores.column("Certificación", width=150)
    tabla_sugeridos_distribuidores.column("Calificación", width=100)
    tabla_sugeridos_distribuidores.column("Estado de Entrega", width=150)

    # Insertar datos en la tabla
    mostrar_distribuidores_sugeridos()

    # Empaquetar la tabla
    tabla_sugeridos_distribuidores.pack(expand=True, fill='both')

#-----------------------------HISTORIAL DISTRIBUIDORES----------------

    # Crear frame para la tabla de historial de distribuidores
    frame_historial = tk.Frame(notebook)
    notebook.add(frame_historial, text="Historial de Distribuidores")

    # Título para la pestaña de historial
    titulo_historial = tk.Label(frame_historial, text="Historial de Distribuidores", font=("Arial", 16))
    titulo_historial.pack(pady=10)

    # Crear frame para la tabla de historial
    frame_tabla_historial = tk.Frame(frame_historial)
    frame_tabla_historial.pack(pady=10)

    # Encabezados de la tabla de historial de distribuidores
    columnas_historial = ("ID", "Nombre", "Certificación", "Contacto", "Calificación", "Eliminado")
    global tabla_historial_distribuidores
    tabla_historial_distribuidores = ttk.Treeview(frame_tabla_historial, columns=columnas_historial, show='headings')

    # Definir encabezados
    for columna in columnas_historial:
        tabla_historial_distribuidores.heading(columna, text=columna)

    # Ancho de columnas
    tabla_historial_distribuidores.column("ID", width=50)
    tabla_historial_distribuidores.column("Nombre", width=150)
    tabla_historial_distribuidores.column("Certificación", width=150)
    tabla_historial_distribuidores.column("Contacto", width=150)
    tabla_historial_distribuidores.column("Calificación", width=100)
    tabla_historial_distribuidores.column("Eliminado", width=80)

    # Insertar datos en la tabla
    mostrar_historial_distribuidores()
    tabla_historial_distribuidores.pack()

    

    root.mainloop()


def modificar_distribuidor():
    seleccion = tabla_distribuidores.focus()
    distribuidor = tabla_distribuidores.item(seleccion, 'values')

    if not distribuidor:
        messagebox.showwarning("Advertencia", "Selecciona un distribuidor para modificar")
        return

    # Extraer los valores actuales del distribuidor
    distribuidor_id = distribuidor[0]
    nombre_actual = distribuidor[1]
    certificacion_actual = distribuidor[2]
    contacto_actual = distribuidor[3]
    calificacion_actual = distribuidor[4]

    def guardar_cambios():
        try:
            # Obtener los datos del distribuidor
            nuevo_nombre = entry_nombre.get()

            # Certificación: Obtener el índice seleccionado y usar el ID asociado.
            certificacion_index = combo_certificacion.current()
            nueva_certificacion_id = certificacion_ids[certificacion_index]

            nuevo_contacto = entry_contacto.get()

            # Obtener los datos de la calificación
            nuevo_comentario = entry_comentario.get()
            try:
                nueva_calificacion_valor = int(entry_calificacion.get())
                if nueva_calificacion_valor < 1 or nueva_calificacion_valor > 5:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "La calificación debe ser un número entre 1 y 5.")
                return

            fecha_calificacion = date_entry_fecha_calificacion.get_date().strftime('%Y-%m-%d')
            cliente = entry_cliente.get()

            # Obtener los datos de la entrega
            nueva_fecha_entrega = date_entry_fecha_entrega.get_date().strftime('%Y-%m-%d')
            nuevo_estado_entrega = combo_estado_entrega.get()

            # Actualizar el distribuidor en la base de datos
            servicios.actualizar_distribuidor(distribuidor_id, nuevo_nombre, nueva_certificacion_id, nuevo_contacto, nueva_calificacion_valor)

            # Actualizar la entrega para el distribuidor
            servicios.actualizar_entrega(distribuidor_id, nueva_fecha_entrega, nuevo_estado_entrega)

            # Actualizar la calificación para el distribuidor
            servicios.actualizar_calificacion(distribuidor_id, nuevo_comentario, nueva_calificacion_valor, fecha_calificacion, cliente)

            top.destroy()
            actualizar_tabla()
            messagebox.showinfo("Éxito", "Distribuidor modificado con éxito")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")

    # Crear ventana para modificar distribuidor
    top = tk.Toplevel()
    top.title("Modificar Distribuidor")

    # Datos del distribuidor
    tk.Label(top, text="Nombre del Distribuidor").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_nombre = tk.Entry(top)
    entry_nombre.insert(0, nombre_actual)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(top, text="Certificación").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    certificaciones = servicios.obtener_certificaciones()
    certificacion_ids = [str(cert[0]) for cert in certificaciones]
    certificacion_nombres = [cert[1] for cert in certificaciones]
    combo_certificacion = ttk.Combobox(top, values=certificacion_nombres)
    combo_certificacion.set(certificacion_actual)
    combo_certificacion.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(top, text="Contacto").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_contacto = tk.Entry(top)
    entry_contacto.insert(0, contacto_actual)
    entry_contacto.grid(row=2, column=1, padx=10, pady=5)

    # Datos de la calificación
    tk.Label(top, text="Comentario de Calificación").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_comentario = tk.Entry(top)
    entry_comentario.insert(0, "Comentario actual")  # Placeholder, reemplaza con valor actual si es necesario
    entry_comentario.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(top, text="Calificación (1-5)").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    entry_calificacion = tk.Entry(top)
    entry_calificacion.insert(0, str(calificacion_actual))  # Valor actual
    entry_calificacion.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(top, text="Fecha de Calificación").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    date_entry_fecha_calificacion = DateEntry(top, date_pattern='y-mm-dd')
    date_entry_fecha_calificacion.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(top, text="Cliente").grid(row=6, column=0, padx=10, pady=5, sticky="e")
    entry_cliente = tk.Entry(top)
    entry_cliente.insert(0, "Cliente actual")  # Placeholder, reemplaza con valor actual si es necesario
    entry_cliente.grid(row=6, column=1, padx=10, pady=5)

    # Datos de la entrega
    tk.Label(top, text="Fecha de Entrega").grid(row=7, column=0, padx=10, pady=5, sticky="e")
    date_entry_fecha_entrega = DateEntry(top, date_pattern='y-mm-dd')
    date_entry_fecha_entrega.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(top, text="Estado de Entrega").grid(row=8, column=0, padx=10, pady=5, sticky="e")
    combo_estado_entrega = ttk.Combobox(top, values=["Completada", "Pendiente"])
    combo_estado_entrega.grid(row=8, column=1, padx=10, pady=5)

    # Botón para guardar
    btn_guardar = tk.Button(top, text="Guardar Cambios", command=guardar_cambios)
    btn_guardar.grid(row=9, column=0, columnspan=2, pady=20)

    centrar_ventana(top)


    
# Función para centrar la ventana en la pantalla
def centrar_ventana(ventana):
    ventana.update_idletasks()
    width = ventana.winfo_width()
    height = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana.winfo_screenheight() // 2) - (height // 2)
    ventana.geometry(f'{width}x{height}+{x}+{y}')


# Función para seleccionar distribuidor y añadirlo a la pestaña "Distribuidores Seleccionados"
def seleccionar_distribuidor():
    seleccion = tabla_distribuidores.focus()
    distribuidor = tabla_distribuidores.item(seleccion, 'values')
    
    if not distribuidor:
        messagebox.showwarning("Advertencia", "Selecciona un distribuidor primero")
        return

    # Verificar si el distribuidor ya fue seleccionado
    if distribuidor in distribuidores_seleccionados:
        messagebox.showinfo("Información", "Este distribuidor ya ha sido seleccionado.")
        return

    # Añadir el distribuidor a la lista de seleccionados y actualizar la tabla de seleccionados
    distribuidores_seleccionados.append(distribuidor)
    tabla_distribuidores_seleccionados.insert("", "end", values=distribuidor)

#------------------ GENERAR REPORTE PDF---------------
def generar_reporte_pdf():
    if not distribuidores_seleccionados:
        messagebox.showwarning("Advertencia", "No hay distribuidores seleccionados para generar el reporte.")
        return

    # Crear el PDF
    pdf = FPDF()
    pdf.add_page()

    # Configurar fuente y título
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Reporte de Distribuidores Seleccionados", ln=True, align='C')
    pdf.ln(10)  # Espacio vertical

    # Agregar encabezados de la tabla
    pdf.set_font("Arial", "B", 10)
    headers = ["ID", "Nombre", "Certificación", "Contacto", "Calificación"]
    col_widths = [20, 40, 60, 60, 20]  # Ancho de las columnas
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, 1, 0, 'C')
    pdf.ln()

    # Agregar datos de distribuidores seleccionados
    pdf.set_font("Arial", "", 10)
    for distribuidor in distribuidores_seleccionados:
        pdf.cell(col_widths[0], 10, str(distribuidor[0]), 1, 0, 'C')  # ID
        pdf.cell(col_widths[1], 10, distribuidor[1], 1, 0, 'C')      # Nombre
        pdf.cell(col_widths[2], 10, distribuidor[2], 1, 0, 'C')      # Certificación
        pdf.cell(col_widths[3], 10, distribuidor[3], 1, 0, 'C')      # Contacto
        pdf.cell(col_widths[4], 10, str(distribuidor[4]), 1, 0, 'C') # Calificación
        pdf.ln()

    # Guardar el archivo PDF
    try:
        pdf.output("reporte_distribuidores_seleccionados.pdf")
        messagebox.showinfo("Éxito", "Reporte PDF generado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar el PDF: {e}")


# Función para cargar las certificaciones del distribuidor seleccionado
def cargar_certificaciones_distribuidor():
    # Obtener el distribuidor seleccionado en la tabla de distribuidores
    seleccion = tabla_distribuidores.focus()
    distribuidor = tabla_distribuidores.item(seleccion, 'values')
    
    if not distribuidor:
        messagebox.showwarning("Advertencia", "Selecciona un distribuidor primero")
        return

    distribuidor_id = distribuidor[0]  # Obtener el ID del distribuidor seleccionado

    # Limpiar tabla de certificaciones
    for row in tabla_certificaciones.get_children():
        tabla_certificaciones.delete(row)

    # Obtener certificaciones del distribuidor (filtradas por el id del distribuidor seleccionado)
    certificaciones = servicios.obtener_certificaciones_distribuidor(distribuidor_id)

    # Insertar certificaciones en la tabla
    for certificacion in certificaciones:
        tabla_certificaciones.insert("", "end", values=certificacion)

# Función para mostrar los distribuidores en la tabla
def mostrar_distribuidores():
    distribuidores = servicios.obtener_distribuidores()
    for distribuidor in distribuidores:
        tabla_distribuidores.insert("", "end", values=distribuidor)

# Función para mostrar los comentarios en la tabla al iniciar o cuando se selecciona la pestaña
def mostrar_comentarios():
    # Limpiar la tabla de comentarios antes de cargar nuevos datos
    for row in tabla_comentarios.get_children():
        tabla_comentarios.delete(row)

    # Obtener todos los comentarios de la base de datos
    comentarios = servicios.obtener_todos_los_comentarios()

    # Insertar los comentarios en la tabla
    for comentario in comentarios:
        tabla_comentarios.insert("", "end", values=comentario)

# Función para cargar las entregas del distribuidor seleccionado
def cargar_entregas_distribuidor():
    # Obtener el distribuidor seleccionado en la tabla de distribuidores
    seleccion = tabla_distribuidores.focus()
    distribuidor = tabla_distribuidores.item(seleccion, 'values')
    distribuidor_id = distribuidor[0]


    # Limpiar tabla de entregas
    for row in tabla_entregas.get_children():
        tabla_entregas.delete(row)

    # Obtener entregas del distribuidor
    entregas = servicios.obtener_entregas_distribuidor(distribuidor_id)

    # Insertar entregas en la tabla
    for entrega in entregas:
        tabla_entregas.insert("", "end", values=entrega)

# Función para cargar los comentarios del distribuidor seleccionado
def cargar_comentarios_distribuidor():
    # Obtener el distribuidor seleccionado
    seleccion = tabla_distribuidores.focus()
    distribuidor = tabla_distribuidores.item(seleccion, 'values')
    
    if not distribuidor:
        messagebox.showwarning("Advertencia", "Selecciona un distribuidor primero")
        return
    
    distribuidor_id = distribuidor[0]  # Obtener el ID del distribuidor seleccionado

    # Limpiar la tabla de comentarios
    for row in tabla_comentarios.get_children():
        tabla_comentarios.delete(row)

    # Obtener los comentarios asociados a este distribuidor
    comentarios = servicios.obtener_comentarios_distribuidor(distribuidor_id)

    # Verificar si hay comentarios y si están siendo insertados correctamente
    if comentarios:
        print(f"Insertando los comentarios en la tabla: {comentarios}")
        for comentario in comentarios:
            tabla_comentarios.insert("", "end", values=comentario)
    else:
        print(f"No se encontraron comentarios para el distribuidor {distribuidor_id}")

# Función para mostrar todas las entregas en la tabla al iniciar o cuando se selecciona la pestaña
def mostrar_entregas():
    # Limpiar la tabla de entregas antes de cargar nuevos datos
    for row in tabla_entregas.get_children():
        tabla_entregas.delete(row)

    # Obtener todas las entregas de la base de datos
    entregas = servicios.obtener_todas_las_entregas()

    # Insertar las entregas en la tabla
    for entrega in entregas:
        tabla_entregas.insert("", "end", values=entrega)

# Función para mostrar todas las certificaciones en la tabla al iniciar o cuando se selecciona la pestaña
def mostrar_certificaciones():
    # Limpiar la tabla de certificaciones antes de cargar nuevos datos
    for row in tabla_certificaciones.get_children():
        tabla_certificaciones.delete(row)

    # Obtener todas las certificaciones de la base de datos
    certificaciones = servicios.obtener_todas_las_certificaciones()

    # Insertar las certificaciones en la tabla
    for certificacion in certificaciones:
        tabla_certificaciones.insert("", "end", values=certificacion)



# Función para buscar distribuidores
def buscar_distribuidor():
    criterio = entry_busqueda.get()
    if criterio:
        distribuidores = servicios.buscar_distribuidores(criterio)
        for row in tabla_distribuidores.get_children():
            tabla_distribuidores.delete(row)
        for distribuidor in distribuidores:
            tabla_distribuidores.insert("", "end", values=distribuidor)
    else:
        messagebox.showwarning("Advertencia", "Ingresa un criterio de búsqueda")

# Función para crear un nuevo distribuidor
def crear_distribuidor():
    def guardar_distribuidor():
        # Obtener los datos del distribuidor
        nombre = entry_nombre.get()

        # Certificación: Obtener el índice seleccionado y usar el ID asociado.
        certificacion_index = combo_certificacion.current()
        certificacion_id = certificacion_ids[certificacion_index]

        contacto = entry_contacto.get()

        # Obtener los datos de la calificación del distribuidor
        comentario = entry_comentario.get()
        try:
            calificacion_valor = int(entry_calificacion.get())
            if calificacion_valor < 1 or calificacion_valor > 5:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La calificación debe ser un número entre 1 y 5.")
            return

        fecha_calificacion = date_entry_fecha_calificacion.get_date().strftime('%Y-%m-%d')
        cliente = entry_cliente.get()

        # Datos de la certificación
        nombre_certificacion = entry_nombre_certificacion.get()
        organismo_emisor = entry_organismo_emisor.get()
        fecha_emision = date_entry_fecha_emision.get_date().strftime('%Y-%m-%d')
        fecha_expiracion = date_entry_fecha_expiracion.get_date().strftime('%Y-%m-%d')

        # Mapea el estado de la certificación a un valor booleano
        estado_certificacion = combo_estado_certificacion.get()
        estado_certificacion_valor = 1 if estado_certificacion == "Válida" else 0

        puntuacion = float(entry_puntuacion.get())

        # Obtener los datos de la entrega
        fecha_entrega = date_entry_fecha_entrega.get_date().strftime('%Y-%m-%d')
        estado_entrega = combo_estado_entrega.get()

        # Insertar el distribuidor
        distribuidor_id = servicios.insertar_distribuidor(nombre, certificacion_id, contacto, calificacion_valor)

        # Insertar la certificación para el distribuidor
        certificacion_id = servicios.insertar_certificacion(nombre_certificacion, organismo_emisor, fecha_emision, fecha_expiracion, estado_certificacion_valor, puntuacion)

        # Insertar la entrega para el distribuidor
        servicios.insertar_entrega(distribuidor_id, fecha_entrega, estado_entrega)

        # Insertar la calificación para el distribuidor
        servicios.insertar_calificacion(distribuidor_id, comentario, calificacion_valor, fecha_calificacion, cliente)

        # Cerrar la ventana y actualizar la tabla
        top.destroy()
        actualizar_tabla()
        messagebox.showinfo("Éxito", "Distribuidor y sus datos insertados con éxito")

    top = tk.Toplevel()
    top.title("Crear Distribuidor")

    # Ajustar el tamaño de la ventana para evitar que sea demasiado grande
    top.geometry("600x600")  # Puedes ajustar el tamaño según sea necesario
    top.columnconfigure(0, weight=1)
    top.columnconfigure(1, weight=1)

    # Datos del distribuidor (Primera columna)
    tk.Label(top, text="Nombre del Distribuidor").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_nombre = tk.Entry(top)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(top, text="Certificación").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    certificaciones = servicios.obtener_certificaciones()
    certificacion_ids = [str(cert[0]) for cert in certificaciones]
    certificacion_nombres = [cert[1] for cert in certificaciones]
    combo_certificacion = ttk.Combobox(top, values=certificacion_nombres)
    combo_certificacion.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(top, text="Contacto").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_contacto = tk.Entry(top)
    entry_contacto.grid(row=2, column=1, padx=10, pady=5)

    # Datos de la calificación (Segunda columna)
    tk.Label(top, text="Comentario de Calificación").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_comentario = tk.Entry(top)
    entry_comentario.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(top, text="Calificación (1-5)").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    entry_calificacion = tk.Entry(top)
    entry_calificacion.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(top, text="Fecha de Calificación").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    date_entry_fecha_calificacion = DateEntry(top, date_pattern='y-mm-dd')
    date_entry_fecha_calificacion.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(top, text="Cliente").grid(row=6, column=0, padx=10, pady=5, sticky="e")
    entry_cliente = tk.Entry(top)
    entry_cliente.grid(row=6, column=1, padx=10, pady=5)

    # Datos de la certificación (Primera columna)
    tk.Label(top, text="Nombre de la Certificación").grid(row=7, column=0, padx=10, pady=5, sticky="e")
    entry_nombre_certificacion = tk.Entry(top)
    entry_nombre_certificacion.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(top, text="Organismo Emisor").grid(row=8, column=0, padx=10, pady=5, sticky="e")
    entry_organismo_emisor = tk.Entry(top)
    entry_organismo_emisor.grid(row=8, column=1, padx=10, pady=5)

    tk.Label(top, text="Fecha de Emisión").grid(row=9, column=0, padx=10, pady=5, sticky="e")
    date_entry_fecha_emision = DateEntry(top, date_pattern='y-mm-dd')
    date_entry_fecha_emision.grid(row=9, column=1, padx=10, pady=5)

    tk.Label(top, text="Fecha de Expiración").grid(row=10, column=0, padx=10, pady=5, sticky="e")
    date_entry_fecha_expiracion = DateEntry(top, date_pattern='y-mm-dd')
    date_entry_fecha_expiracion.grid(row=10, column=1, padx=10, pady=5)

    tk.Label(top, text="Estado de la Certificación").grid(row=11, column=0, padx=10, pady=5, sticky="e")
    combo_estado_certificacion = ttk.Combobox(top, values=["Válida", "Expirada"])
    combo_estado_certificacion.grid(row=11, column=1, padx=10, pady=5)

    tk.Label(top, text="Puntuación de la Certificación").grid(row=12, column=0, padx=10, pady=5, sticky="e")
    entry_puntuacion = tk.Entry(top)
    entry_puntuacion.grid(row=12, column=1, padx=10, pady=5)

    # Datos de la entrega (Segunda columna)
    tk.Label(top, text="Fecha de Entrega").grid(row=13, column=0, padx=10, pady=5, sticky="e")
    date_entry_fecha_entrega = DateEntry(top, date_pattern='y-mm-dd')
    date_entry_fecha_entrega.grid(row=13, column=1, padx=10, pady=5)

    tk.Label(top, text="Estado de Entrega").grid(row=14, column=0, padx=10, pady=5, sticky="e")
    combo_estado_entrega = ttk.Combobox(top, values=["Completada", "Pendiente"])
    combo_estado_entrega.grid(row=14, column=1, padx=10, pady=5)

    # Botón para guardar, centrado al final
    btn_guardar = tk.Button(top, text="Guardar", command=guardar_distribuidor)
    btn_guardar.grid(row=15, column=0, columnspan=2, pady=20)

    centrar_ventana(top)



# Función para eliminar un distribuidor (soft delete)
def eliminar_distribuidor_ui():
    seleccion = tabla_distribuidores.focus()
    distribuidor = tabla_distribuidores.item(seleccion, 'values')
    distribuidor_id = distribuidor[0]

    # Actualizar el campo "eliminado" a True
    servicios.eliminar_distribuidor_logico(distribuidor_id)
    
    actualizar_tabla()
    messagebox.showinfo("Éxito", "Distribuidor marcado como eliminado con éxito")



# Función para mostrar el historial de distribuidores
def mostrar_historial_distribuidores():
    # Limpiar la tabla de historial
    for row in tabla_historial_distribuidores.get_children():
        tabla_historial_distribuidores.delete(row)

    # Obtener todos los distribuidores (incluyendo los eliminados)
    distribuidores_historial = servicios.obtener_historial_distribuidores()

    # Insertar distribuidores en la tabla
    for distribuidor in distribuidores_historial:
        tabla_historial_distribuidores.insert("", "end", values=distribuidor)

# Actualizar los datos de la tabla
def actualizar_tabla():
    for row in tabla_distribuidores.get_children():
        tabla_distribuidores.delete(row)
    mostrar_distribuidores()

# Función para mostrar los distribuidores sugeridos en la tabla
def mostrar_distribuidores_sugeridos():
    # Acceder a la tabla global
    global tabla_sugeridos_distribuidores

    # Obtener los distribuidores sugeridos desde la base de datos
    distribuidores_sugeridos = servicios.obtener_distribuidores_sugeridos()
    print("Distribuidores sugeridos obtenidos:", distribuidores_sugeridos)

    # Limpiar la tabla si ya contiene datos
    for item in tabla_sugeridos_distribuidores.get_children():
        tabla_sugeridos_distribuidores.delete(item)

    # Insertar los distribuidores sugeridos en la tabla
    for distribuidor in distribuidores_sugeridos:
        print(f"Insertando en Treeview: {distribuidor}")  # Verificación adicional
        tabla_sugeridos_distribuidores.insert('', 'end', values=distribuidor)

    # Para pruebas, puedes agregar un distribuidor manualmente y ver si se muestra
    tabla_sugeridos_distribuidores.insert('', 'end', values=(1, 'Distribuidor Prueba', 'ISO 9001', 5, 'Completada'))
