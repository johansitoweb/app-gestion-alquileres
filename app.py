import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import time

# Conexión a la base de datos SQLite
def conectar_db():
    conn = sqlite3.connect('alquileres.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            usuario TEXT NOT NULL UNIQUE,
            contraseña TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS propiedades (
            id INTEGER PRIMARY KEY,
            direccion TEXT NOT NULL,
            inquilino TEXT,
            pago REAL,
            fecha_pago DATE,
            descripcion TEXT
        )
    ''')
    conn.commit()
    return conn

# Función para simular la carga
def cargar():
    for i in range(101):
        barra_progreso['value'] = i
        ventana.update()
        time.sleep(0.090)  # Simula tiempo de carga
    ventana.destroy()  # Cierra la ventana de carga
    abrir_login()  # Abre la ventana de login

# Función para abrir la ventana de login
def abrir_login():
    login_window = tk.Tk()
    login_window.title("Iniciar Sesión")

    tk.Label(login_window, text="Usuario:").pack()
    usuario_entry = tk.Entry(login_window)
    usuario_entry.pack()

    tk.Label(login_window, text="Contraseña:").pack()
    contraseña_entry = tk.Entry(login_window, show="*")
    contraseña_entry.pack()

    tk.Button(login_window, text="Iniciar Sesión", command=lambda: iniciar_sesion(usuario_entry.get(), contraseña_entry.get())).pack()
    tk.Button(login_window, text="Crear Cuenta", command=crear_cuenta).pack(pady=10)
    login_window.mainloop()

# Función para crear una nueva cuenta
def crear_cuenta():
    def guardar_cuenta():
        usuario = usuario_entry.get()
        contraseña = contraseña_entry.get()

        conn = conectar_db()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)', (usuario, contraseña))
            conn.commit()
            messagebox.showinfo("Éxito", "Cuenta creada exitosamente")
            crear_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El usuario ya existe")
        finally:
            conn.close()

    crear_window = tk.Toplevel()
    crear_window.title("Crear Cuenta")

    tk.Label(crear_window, text="Usuario:").pack()
    usuario_entry = tk.Entry(crear_window)
    usuario_entry.pack()

    tk.Label(crear_window, text="Contraseña:").pack()
    contraseña_entry = tk.Entry(crear_window, show="*")
    contraseña_entry.pack()

    tk.Button(crear_window, text="Guardar", command=guardar_cuenta).pack()

# Función para iniciar sesión
def iniciar_sesion(usuario, contraseña):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE usuario=? AND contraseña=?', (usuario, contraseña))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
        abrir_ventana_principal()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Función para abrir la ventana principal
def abrir_ventana_principal():
    main_window = tk.Tk()
    main_window.title("Gestión de Alquileres")

    # Botones para funcionalidades
    tk.Button(main_window, text="Añadir Propiedad", command=anadir_propiedad).pack(pady=10)
    tk.Button(main_window, text="Ver Propiedades", command=ver_propiedades).pack(pady=10)
    tk.Button(main_window, text="Calendario de Pagos", command=calendario_pagos).pack(pady=10)
    tk.Button(main_window, text="Contratos Electrónicos", command=contratos_electronicos).pack(pady=10)

    main_window.mainloop()

# Función para añadir propiedad
def anadir_propiedad():
    def guardar_propiedad():
        direccion = direccion_entry.get()
        inquilino = inquilino_entry.get()
        pago = float(pago_entry.get())
        fecha_pago = fecha_pago_entry.get()
        descripcion = descripcion_entry.get()

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO propiedades (direccion, inquilino, pago, fecha_pago, descripcion) VALUES (?, ?, ?, ?, ?)',
                       (direccion, inquilino, pago, fecha_pago, descripcion))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Propiedad añadida exitosamente")
        anadir_window.destroy()

    anadir_window = tk.Toplevel()
    anadir_window.title("Añadir Propiedad")

    tk.Label(anadir_window, text="Dirección:").pack()
    direccion_entry = tk.Entry(anadir_window)
    direccion_entry.pack()

    tk.Label(anadir_window, text="Inquilino:").pack()
    inquilino_entry = tk.Entry(anadir_window)
    inquilino_entry.pack()

    tk.Label(anadir_window, text="Pago:").pack()
    pago_entry = tk.Entry(anadir_window)
    pago_entry.pack()

    tk.Label(anadir_window, text="Fecha de Pago (YYYY-MM-DD):").pack()
    fecha_pago_entry = tk.Entry(anadir_window)
    fecha_pago_entry.pack()

    tk.Label(anadir_window, text="Descripción:").pack()
    descripcion_entry = tk.Entry(anadir_window)
    descripcion_entry.pack()

    tk.Button(anadir_window, text="Guardar", command=guardar_propiedad).pack()

# Función para ver propiedades
def ver_propiedades():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM propiedades')
    propiedades = cursor.fetchall()
    conn.close()

    ver_window = tk.Toplevel()
    ver_window.title("Propiedades")

    for propiedad in propiedades:
        frame = tk.Frame(ver_window)
        frame.pack(pady=5)

        tk.Label(frame, text=f"ID: {propiedad[0]}, Dirección: {propiedad[1]}, Inquilino: {propiedad[2]}, Pago: {propiedad[3]}, Fecha de Pago: {propiedad[4]}, Descripción: {propiedad[5]}").pack(side=tk.LEFT)
        tk.Button(frame, text="Editar", command=lambda p=propiedad: editar_propiedad(p)).pack(side=tk.RIGHT)

# Función para editar propiedad
def editar_propiedad(propiedad):
    def guardar_edicion():
        direccion = direccion_entry.get()
        inquilino = inquilino_entry.get()
        pago = float(pago_entry.get())
        fecha_pago = fecha_pago_entry.get()
        descripcion = descripcion_entry.get()

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE propiedades SET direccion=?, inquilino=?, pago=?, fecha_pago=?, descripcion=? WHERE id=?',
                       (direccion, inquilino, pago, fecha_pago, descripcion, propiedad[0]))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Propiedad actualizada exitosamente")
        editar_window.destroy()
        ver_propiedades()  # Actualiza la lista de propiedades

    editar_window = tk.Toplevel()
    editar_window.title("Editar Propiedad")

    tk.Label(editar_window, text="Dirección:").pack()
    direccion_entry = tk.Entry(editar_window)
    direccion_entry.insert(0, propiedad[1])
    direccion_entry.pack()

    tk.Label(editar_window, text="Inquilino:").pack()
    inquilino_entry = tk.Entry(editar_window)
    inquilino_entry.insert(0, propiedad[2])
    inquilino_entry.pack()

    tk.Label(editar_window, text="Pago:").pack()
    pago_entry = tk.Entry(editar_window)
    pago_entry.insert(0, propiedad[3])
    pago_entry.pack()

    tk.Label(editar_window, text="Fecha de Pago (YYYY-MM-DD):").pack()
    fecha_pago_entry = tk.Entry(editar_window)
    fecha_pago_entry.insert(0, propiedad[4])
    fecha_pago_entry.pack()

    tk.Label(editar_window, text="Descripción:").pack()
    descripcion_entry = tk.Entry(editar_window)
    descripcion_entry.insert(0, propiedad[5])
    descripcion_entry.pack()

    tk.Button(editar_window, text="Guardar Cambios", command=guardar_edicion).pack()

# Función para mostrar calendario de pagos
def calendario_pagos():
    calendario_window = tk.Toplevel()
    calendario_window.title("Calendario de Pagos")
    tk.Label(calendario_window, text="Aquí puedes implementar un calendario de pagos.").pack()

# Función para manejar contratos electrónicos
def contratos_electronicos():
    contratos_window = tk.Toplevel()
    contratos_window.title("Contratos Electrónicos")
    tk.Label(contratos_window, text="Aquí puedes implementar la gestión de contratos electrónicos.").pack()

# Crear la ventana de carga
ventana = tk.Tk()
ventana.title("Cargando")
ventana.geometry("300x100")
ventana.configure(bg='lightgreen')  # Cambiar el color de fondo

tk.Label(ventana, text="Sistema de Alquiler", bg='lightgreen', font=("Arial", 16)).pack(pady=10)

barra_progreso = ttk.Progressbar(ventana, length=200, mode='determinate')
barra_progreso.pack(pady=20)

# Iniciar la carga
cargar()

ventana.mainloop()
