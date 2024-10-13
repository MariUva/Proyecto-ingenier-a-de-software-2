import tkinter as tk
from tkinter import ttk
from services.gestion_entregas import insertar_distribuidor, eliminar_distribuidor, actualizar_distribuidor, obtener_distribuidores

# Función para centrar la ventana en la pantalla
def centrar_ventana(ventana):
    ventana.update_idletasks()
    width = ventana.winfo_width()
    height = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana.winfo_screenheight() // 2) - (height // 2)
    ventana.geometry(f'{width}x{height}+{x}+{y}')

# Función para mostrar los distribuidores en la tabla
def mostrar_distribuidores():
    distribuidores = obtener_distribuidores()
    for distribuidor in distribuidores:
        tabla.insert("", "end", values=distribuidor)

# Función para crear un nuevo distribuidor
def crear_distribuidor():
    def guardar_distribuidor():
        nombre = entry_nombre.get()
        certificacion = entry_certificacion.get()
        contacto = entry_contacto.get()
        calificacion = int(entry_calificacion.get())
        insertar_distribuidor(nombre, certificacion, contacto, calificacion)
        top.destroy()
        actualizar_tabla()  # Actualiza la tabla después de insertar

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
    centrar_ventana(top)  # Centrar la ventana secundaria

# Función para modificar un distribuidor
def modificar_distribuidor():
    seleccion = tabla.focus()
    distribuidor = tabla.item(seleccion, 'values')
    
    def guardar_cambios():
        distribuidor_id = distribuidor[0]
        nuevo_nombre = entry_nombre.get()
        nueva_certificacion = entry_certificacion.get()
        nuevo_contacto = entry_contacto.get()
        nueva_calificacion = int(entry_calificacion.get())
        actualizar_distribuidor(distribuidor_id, nuevo_nombre, nueva_certificacion, nuevo_contacto, nueva_calificacion)
        top.destroy()
        actualizar_tabla()  # Actualiza la tabla después de modificar

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
    centrar_ventana(top)  # Centrar la ventana secundaria

# Función para eliminar un distribuidor
def eliminar_distribuidor_ui():
    seleccion = tabla.focus()
    distribuidor = tabla.item(seleccion, 'values')
    distribuidor_id = distribuidor[0]
    eliminar_distribuidor(distribuidor_id)
    actualizar_tabla()  # Actualiza la tabla después de eliminar

# Actualizar los datos de la tabla
def actualizar_tabla():
    # Limpiar la tabla
    for row in tabla.get_children():
        tabla.delete(row)
    # Volver a cargar los distribuidores
    mostrar_distribuidores()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Gestión de Distribuidores")
root.geometry("800x400")

# Centrar la ventana principal
centrar_ventana(root)

# Título
titulo = tk.Label(root, text="Gestión de Distribuidores", font=("Arial", 16))
titulo.pack(pady=10)

# Crear frame para la tabla
frame_tabla = tk.Frame(root)
frame_tabla.pack(pady=10)

# Encabezados de la tabla
columnas = ("ID", "Nombre", "Certificación", "Contacto", "Calificación")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show='headings')

# Definir encabezados
for columna in columnas:
    tabla.heading(columna, text=columna)

# Ancho de columnas
tabla.column("ID", width=50)
tabla.column("Nombre", width=150)
tabla.column("Certificación", width=150)
tabla.column("Contacto", width=150)
tabla.column("Calificación", width=100)

# Insertar datos en la tabla
mostrar_distribuidores()
tabla.pack()

# Crear frame para los botones de CRUD
frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

# Botones CRUD con colores
btn_crear = tk.Button(frame_botones, text="Crear Distribuidor", command=crear_distribuidor, bg="green", fg="white")
btn_crear.grid(row=0, column=0, padx=10)

btn_modificar = tk.Button(frame_botones, text="Modificar Distribuidor", command=modificar_distribuidor, bg="blue", fg="white")
btn_modificar.grid(row=0, column=1, padx=10)

btn_eliminar = tk.Button(frame_botones, text="Eliminar Distribuidor", command=eliminar_distribuidor_ui, bg="red", fg="white")
btn_eliminar.grid(row=0, column=2, padx=10)

root.mainloop()
