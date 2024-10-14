import tkinter as tk
from tkinter import ttk, messagebox
from servicios import Servicios

# Inicializar la clase Servicios para conectar a la base de datos

servicios = Servicios()

# Variable global para almacenar el distribuidor seleccionado
distribuidor_seleccionado = None

def iniciar_gui():
    root = tk.Tk()
    root.title("Gestión de Distribuidores")
    root.geometry("800x400")

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

    # Crear frame para los botones de CRUD
    frame_botones = tk.Frame(frame_distribuidores)
    frame_botones.pack(pady=10)

    # Botones CRUD con colores
    btn_crear = tk.Button(frame_botones, text="Crear Distribuidor", command=crear_distribuidor, bg="green", fg="white")
    btn_crear.grid(row=0, column=0, padx=10)

    btn_modificar = tk.Button(frame_botones, text="Modificar Distribuidor", command=modificar_distribuidor, bg="blue", fg="white")
    btn_modificar.grid(row=0, column=1, padx=10)

    btn_eliminar = tk.Button(frame_botones, text="Eliminar Distribuidor", command=eliminar_distribuidor_ui, bg="red", fg="white")
    btn_eliminar.grid(row=0, column=2, padx=10)

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

    # Botón para cargar certificaciones de un distribuidor seleccionado
    btn_cargar_certificaciones = tk.Button(frame_certificaciones, text="Cargar Certificaciones", command=cargar_certificaciones_distribuidor, bg="yellow", fg="black")
    btn_cargar_certificaciones.pack(pady=10)

    root.mainloop()

# Función para centrar la ventana en la pantalla
def centrar_ventana(ventana):
    ventana.update_idletasks()
    width = ventana.winfo_width()
    height = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana.winfo_screenheight() // 2) - (height // 2)
    ventana.geometry(f'{width}x{height}+{x}+{y}')

# Función para cargar las certificaciones del distribuidor seleccionado
def cargar_certificaciones_distribuidor():
    # Obtener el distribuidor seleccionado en la tabla de distribuidores
    seleccion = tabla_distribuidores.focus()
    distribuidor = tabla_distribuidores.item(seleccion, 'values')
    distribuidor_id = distribuidor[0]

    # Limpiar tabla de certificaciones
    for row in tabla_certificaciones.get_children():
        tabla_certificaciones.delete(row)

    # Obtener certificaciones del distribuidor
    certificaciones = servicios.obtener_certificaciones_distribuidor(distribuidor_id)

    # Insertar certificaciones en la tabla
    for certificacion in certificaciones:
        tabla_certificaciones.insert("", "end", values=certificacion)

# Función para mostrar los distribuidores en la tabla
def mostrar_distribuidores():
    distribuidores = servicios.obtener_distribuidores()
    for distribuidor in distribuidores:
        tabla_distribuidores.insert("", "end", values=distribuidor)

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
    # Obtener el distribuidor seleccionado en la tabla de distribuidores
    seleccion = tabla_distribuidores.focus()
    distribuidor = tabla_distribuidores.item(seleccion, 'values')
    distribuidor_id = distribuidor[0]

    # Limpiar tabla de comentarios
    for row in tabla_comentarios.get_children():
        tabla_comentarios.delete(row)

    # Obtener comentarios del distribuidor
    comentarios = servicios.obtener_comentarios_distribuidor(distribuidor_id)

    # Insertar comentarios en la tabla
    for comentario in comentarios:
        tabla_comentarios.insert("", "end", values=comentario)


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
        nombre = entry_nombre.get()
        certificacion = entry_certificacion.get()
        contacto = entry_contacto.get()
        calificacion = int(entry_calificacion.get())
        servicios.insertar_distribuidor(nombre, certificacion, contacto, calificacion)
        top.destroy()
        actualizar_tabla()
        messagebox.showinfo("Éxito", "Distribuidor insertado con éxito")

    top = tk.Toplevel()
    top.title("Crear Distribuidor")

    tk.Label(top, text="Nombre").pack()
    entry_nombre = tk.Entry(top)
    entry_nombre.pack()

    tk.Label(top, text="Certificación").pack()
    entry_certificacion = tk.Entry(top)
    entry_certificacion.pack()

    tk.Label(top, text="Contacto").pack()
    entry_contacto = tk.Entry(top)
    entry_contacto.pack()

    tk.Label(top, text="Calificación").pack()
    entry_calificacion = tk.Entry(top)
    entry_calificacion.pack()

    btn_guardar = tk.Button(top, text="Guardar", command=guardar_distribuidor)
    btn_guardar.pack()
    centrar_ventana(top)

# Función para modificar un distribuidor
def modificar_distribuidor():
    seleccion = tabla_distribuidores.focus()
    distribuidor = tabla_distribuidores.item(seleccion, 'values')

    def guardar_cambios():
        distribuidor_id = distribuidor[0]
        nuevo_nombre = entry_nombre.get()
        nueva_certificacion = entry_certificacion.get()
        nuevo_contacto = entry_contacto.get()
        nueva_calificacion = int(entry_calificacion.get())
        servicios.actualizar_distribuidor(distribuidor_id, nuevo_nombre, nueva_certificacion, nuevo_contacto, nueva_calificacion)
        top.destroy()
        actualizar_tabla()
        messagebox.showinfo("Éxito", "Distribuidor actualizado con éxito")

    top = tk.Toplevel()
    top.title("Modificar Distribuidor")

    tk.Label(top, text="Nuevo Nombre").pack()
    entry_nombre = tk.Entry(top)
    entry_nombre.insert(0, distribuidor[1])
    entry_nombre.pack()

    tk.Label(top, text="Nueva Certificación").pack()
    entry_certificacion = tk.Entry(top)
    entry_certificacion.insert(0, distribuidor[2])
    entry_certificacion.pack()

    tk.Label(top, text="Nuevo Contacto").pack()
    entry_contacto = tk.Entry(top)
    entry_contacto.insert(0, distribuidor[3])
    entry_contacto.pack()

    tk.Label(top, text="Nueva Calificación").pack()
    entry_calificacion = tk.Entry(top)
    entry_calificacion.insert(0, distribuidor[4])
    entry_calificacion.pack()

    btn_guardar = tk.Button(top, text="Guardar Cambios", command=guardar_cambios)
    btn_guardar.pack()
    centrar_ventana(top)

# Función para eliminar un distribuidor
def eliminar_distribuidor_ui():
    seleccion = tabla_distribuidores.focus()
    distribuidor = tabla_distribuidores.item(seleccion, 'values')
    distribuidor_id = distribuidor[0]
    servicios.eliminar_distribuidor(distribuidor_id)
    actualizar_tabla()
    messagebox.showinfo("Éxito", "Distribuidor eliminado con éxito")

# Actualizar los datos de la tabla
def actualizar_tabla():
    for row in tabla_distribuidores.get_children():
        tabla_distribuidores.delete(row)
    mostrar_distribuidores()
