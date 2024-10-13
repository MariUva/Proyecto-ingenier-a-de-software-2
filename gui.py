import tkinter as tk
from services.gestion_entregas import insertar_distribuidor, eliminar_distribuidor, actualizar_distribuidor, obtener_distribuidores

# Función para iniciar la interfaz gráfica
def iniciar_gui():
    root = tk.Tk()
    root.title("Sistema de Gestión de Distribuidores")

    # Botón para mostrar distribuidores
    btn_mostrar = tk.Button(root, text="Mostrar Distribuidores", command=mostrar_distribuidores)
    btn_mostrar.pack()

    # Botón para abrir la ventana de creación de distribuidor
    btn_crear = tk.Button(root, text="Crear Distribuidor", command=crear_distribuidor)
    btn_crear.pack()

    # Botón para abrir la ventana de eliminación de distribuidor
    btn_eliminar = tk.Button(root, text="Eliminar Distribuidor", command=eliminar_distribuidor_ui)
    btn_eliminar.pack()

    # Botón para abrir la ventana de modificación de distribuidor
    btn_modificar = tk.Button(root, text="Modificar Distribuidor", command=modificar_distribuidor_ui)
    btn_modificar.pack()

    root.mainloop()

# Función para mostrar distribuidores (solo imprime en consola, puedes modificar para mostrar en GUI)
def mostrar_distribuidores():
    distribuidores = obtener_distribuidores()
    if distribuidores:
        for distribuidor in distribuidores:
            print(distribuidor)  # Puedes mostrarlo en un Listbox o Label en la GUI

# Función para crear un nuevo distribuidor
def crear_distribuidor():
    def guardar_distribuidor():
        nombre = entry_nombre.get()
        certificacion = entry_certificacion.get()
        contacto = entry_contacto.get()
        calificacion = int(entry_calificacion.get())
        
        # Llamada a la función de servicio para guardar el distribuidor
        insertar_distribuidor(nombre, certificacion, contacto, calificacion)
        top.destroy()

    # Crear una ventana secundaria para ingresar el distribuidor
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

    # Botón para guardar el distribuidor
    btn_guardar = tk.Button(top, text="Guardar", command=guardar_distribuidor)
    btn_guardar.pack()

# Función para eliminar un distribuidor
def eliminar_distribuidor_ui():
    def eliminar():
        distribuidor_id = entry_id.get()
        eliminar_distribuidor(distribuidor_id)  # Llamada al servicio para eliminar el distribuidor
        top.destroy()

    # Crear una ventana secundaria para ingresar el ID del distribuidor a eliminar
    top = tk.Toplevel()
    top.title("Eliminar Distribuidor")

    tk.Label(top, text="ID del Distribuidor").pack()
    entry_id = tk.Entry(top)
    entry_id.pack()

    # Botón para eliminar el distribuidor
    btn_eliminar = tk.Button(top, text="Eliminar", command=eliminar)
    btn_eliminar.pack()

# Función para modificar un distribuidor
def modificar_distribuidor_ui():
    def guardar_cambios():
        distribuidor_id = entry_id.get()
        nuevo_nombre = entry_nombre.get()
        nueva_certificacion = entry_certificacion.get()
        nuevo_contacto = entry_contacto.get()
        nueva_calificacion = int(entry_calificacion.get())
        
        # Llamar a la función de servicio para actualizar el distribuidor
        actualizar_distribuidor(distribuidor_id, nuevo_nombre, nueva_certificacion, nuevo_contacto, nueva_calificacion)
        top.destroy()

    # Crear una ventana secundaria para ingresar los nuevos datos
    top = tk.Toplevel()
    top.title("Modificar Distribuidor")

    tk.Label(top, text="ID del Distribuidor").pack()
    entry_id = tk.Entry(top)
    entry_id.pack()

    tk.Label(top, text="Nuevo Nombre").pack()
    entry_nombre = tk.Entry(top)
    entry_nombre.pack()

    tk.Label(top, text="Nueva Certificación").pack()
    entry_certificacion = tk.Entry(top)
    entry_certificacion.pack()

    tk.Label(top, text="Nuevo Contacto").pack()
    entry_contacto = tk.Entry(top)
    entry_contacto.pack()

    tk.Label(top, text="Nueva Calificación").pack()
    entry_calificacion = tk.Entry(top)
    entry_calificacion.pack()

    # Botón para guardar los cambios
    btn_guardar = tk.Button(top, text="Guardar Cambios", command=guardar_cambios)
    btn_guardar.pack()

# Llamada principal para iniciar la GUI
iniciar_gui()
