import tkinter as tk
from services.gestion_entregas import obtener_distribuidores

def mostrar_distribuidores():
    distribuidores = obtener_distribuidores()
    if distribuidores:
        for distribuidor in distribuidores:
            listbox.insert(tk.END, distribuidor)

def iniciar_gui():
    global listbox  # Esto permite que 'listbox' sea accesible dentro de 'mostrar_distribuidores'
    
    root = tk.Tk()
    root.title("Sistema de Compras")

    listbox = tk.Listbox(root)
    listbox.pack()

    btn_mostrar = tk.Button(root, text="Mostrar distribuidores", command=mostrar_distribuidores)
    btn_mostrar.pack()

    root.mainloop()
