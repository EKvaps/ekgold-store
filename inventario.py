import tkinter as tk
from tkinter import messagebox
import json
import os
import subprocess
import webbrowser

# ---------------- CONFIG ----------------

REPO_PATH = r"C:\Users\allsp\OneDrive\Desktop\bienvenida-ekvaps.py - Acceso directo.lnk"
WEB_URL = "https://ekvaps.github.io/ekvaps-store/"
JSON_FILE = os.path.join(REPO_PATH, "inventario.json")

# ---------------- FUNCIONES ----------------

def cargar_inventario():
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_inventario(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def actualizar_lista():
    lista.delete(0, tk.END)
    inventario = cargar_inventario()

    for p in inventario:
        estado = "✔ Disponible" if p["stock"] > 0 else "❌ Agotado"
        lista.insert(
            tk.END,
            f'{p["nombre"]} | Puffs: {p["puffs"]} | Stock: {p["stock"]} | ${p["precio"]} | {estado}'
        )

def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_puffs.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_stock.delete(0, tk.END)
    entry_imagen.delete(0, tk.END)

def añadir_producto():
    nombre = entry_nombre.get().strip()
    puffs = entry_puffs.get().strip()
    precio = entry_precio.get().strip()
    stock = entry_stock.get().strip()
    imagen = entry_imagen.get().strip()

    if not nombre or not precio or not stock:
        messagebox.showerror("Error", "Nombre, precio y stock son obligatorios")
        return

    try:
        stock = int(stock)
    except:
        messagebox.showerror("Error", "Stock debe ser número")
        return

    inventario = cargar_inventario()

    inventario.append({
        "nombre": nombre,
        "puffs": puffs if puffs else "??????",
        "precio": precio,
        "stock": stock,
        "imagen": imagen if imagen else ""
    })

    guardar_inventario(inventario)
    actualizar_lista()
    limpiar_campos()
    messagebox.showinfo("OK", "Producto añadido ✅")

def refrescar_pagina():
    try:
        subprocess.run(["git", "add", "."], cwd=REPO_PATH, check=True)
        subprocess.run(["git", "commit", "-m", "Actualización inventario"], cwd=REPO_PATH, check=True)
        subprocess.run(["git", "push"], cwd=REPO_PATH, check=True)

        messagebox.showinfo("GitHub", "Página actualizada 🚀")

    except subprocess.CalledProcessError:
        messagebox.showwarning("Git", "No hubo cambios o falló git")

def ver_web():
    webbrowser.open(WEB_URL)

# ---------------- UI ----------------

root = tk.Tk()
root.title("Inventario EKvaps")
root.geometry("600x650")
root.configure(bg="black")

titulo = tk.Label(
    root,
    text="Inventario EKvaps",
    font=("Arial", 22, "bold"),
    fg="gold",
    bg="black"
)
titulo.pack(pady=15)

frame_inputs = tk.Frame(root, bg="black")
frame_inputs.pack(pady=10)

def crear_campo(texto, fila):
    tk.Label(frame_inputs, text=texto, fg="white", bg="black").grid(row=fila, column=0, sticky="w")
    entry = tk.Entry(frame_inputs, width=35)
    entry.grid(row=fila, column=1, pady=5)
    return entry

entry_nombre = crear_campo("Nombre:", 0)
entry_puffs = crear_campo("Puffs:", 1)
entry_precio = crear_campo("Precio:", 2)
entry_stock = crear_campo("Stock:", 3)
entry_imagen = crear_campo("Imagen URL:", 4)

btn_add = tk.Button(
    root,
    text="➕ Añadir producto",
    bg="gold",
    fg="black",
    font=("Arial", 12, "bold"),
    width=25,
    command=añadir_producto
)
btn_add.pack(pady=10)

lista = tk.Listbox(
    root,
    width=85,
    height=15,
    bg="#111",
    fg="gold",
    selectbackground="gold",
    selectforeground="black"
)
lista.pack(pady=15)

btn_actualizar = tk.Button(
    root,
    text="🔁 Actualizar lista",
    bg="gold",
    fg="black",
    font=("Arial", 11, "bold"),
    width=25,
    command=actualizar_lista
)
btn_actualizar.pack(pady=5)

btn_refresh = tk.Button(
    root,
    text="🔄 Refrescar Página",
    bg="#444",
    fg="white",
    font=("Arial", 11, "bold"),
    width=25,
    command=refrescar_pagina
)
btn_refresh.pack(pady=10)

btn_web = tk.Button(
    root,
    text="🌐 Ver Web",
    bg="gold",
    fg="black",
    font=("Arial", 11, "bold"),
    width=25,
    command=ver_web
)
btn_web.pack(pady=5)

actualizar_lista()

root.mainloop()
