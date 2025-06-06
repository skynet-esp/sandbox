import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import random

class Interfaz:
    def __init__(self, root, modelo, ejercicios):
        print("Inicializando Interfaz...")
        self.root = root
        self.modelo = modelo
        self.ejercicios = ejercicios
        self.calendar = None
        self.selected_week = None
        self.sincronizando = False
        self.root.title("Entreno Verano")
        self.root.geometry("900x700")
        self.root.configure(bg="#f9fafb")
        self.crear_interfaz()

    def generar_imagen_recompensa(self, recompensa):
        print(f"Generando imagen para recompensa: {recompensa}")
        try:
            img = Image.new('RGB', (200, 200), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except Exception:
                print("Fuente Arial no disponible, usando por defecto")
            if recompensa == "Crack":
                draw.rectangle((80, 60, 120, 100), fill=(255, 215, 0))  # Copa dorada
                draw.ellipse((70, 20, 130, 50), fill=(255, 215, 0))
                draw.text((30, 120), "¡Crack!", font=font, fill="#000000")
            elif recompensa == "Chill":
                for pos in [(60, 60), (140, 60), (100, 100)]:  # Estrellas
                    draw.polygon([
                        (pos[0], pos[1]-15), (pos[0]+5, pos[1]-5),
                        (pos[0]+15, pos[1]-5), (pos[0]+5, pos[1]+5),
                        (pos[0]+10, pos[1]+15), (pos[0], pos[1]+5),
                        (pos[0]-10, pos[1]+15), (pos[0]-5, pos[1]+5),
                        (pos[0]-15, pos[1]-5), (pos[0]-5, pos[1]-5)
                    ], fill=(255, 255, 0))
                draw.text((30, 140), "¡Chill!", font=font, fill="#000000")
            elif recompensa == "Looser":
                draw.ellipse((70, 70, 130, 130), fill=(255, 223, 0))  # Círculo amarillo
                draw.text((30, 140), "¡Looser!", font=font, fill="#000000")
            elif recompensa == "Noob":
                draw.ellipse((70, 50, 130, 110), fill=(220, 220, 220))  # Calavera gris
                draw.text((10, 140), "¡Noob!", font=font, fill="#555")
            img_path = f"temp_{recompensa}.png"
            img.save(img_path)
            imagen = Image.open(img_path)
            imagen = imagen.resize((100, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(imagen)
            return photo, img_path
        except Exception as e:
            print(f"Error al generar imagen: {e}")
            return None, None

    def get_week_dates(self, week_number, year):
        try:
            first_day = datetime.strptime(f"{year}-W{week_number-1}-1", "%Y-W%W-%w").date()
            last_day = first_day + timedelta(days=6)
            return first_day.strftime("%d/%m"), last_day.strftime("%d/%m")
        except Exception as e:
            print(f"Error en get_week_dates: {e}")
            return "N/A", "N/A"

    def get_frase_diaria(self, puntos_dia):
        if puntos_dia <= 10:
            frases = [
                "¡Hoy es un nuevo comienzo, pequeño héroe! 💪",
                "¡Vamos, que cada día es una nueva aventura! 🦸",
                "¡Un pasito hoy, un salto gigante mañana! 🚶"
            ]
        elif puntos_dia <= 25:
            frases = [
                "¡Vas por buen camino, campeón! 🚀",
                "¡Eres un crack, sigue dando caña! 💥",
                "¡Buen trabajo, pequeño titán! 🏋️"
            ]
        else:
            frases = [
                "¡Eres una máquina, sigue así! 🔥",
                "¡Imparable! ¡El gimnasio tiembla contigo! 💪",
                "¡Wow, eres el MVP del día! 🏆"
            ]
        return random.choice(frases)

    def get_frase_semanal(self, puntos, km_corridos, meta_km, completados_total):
        print(f"Generando frase semanal: puntos={puntos}, km_corridos={km_corridos}, meta_km={meta_km}, completados={completados_total}")
        if puntos < 100:
            nivel_puntos = "bajo"
            frases_puntos = [
                "¡Ánimo, esta semana fue un calentamiento! 💪 Vamos a darlo todo la próxima.",
                "No te rindas, cada pequeño esfuerzo cuenta. ¡A por más esta semana! 🔥",
                "¡Toca remontar, campeón! Cada día es una nueva oportunidad para brillar. 🌟"
            ]
        elif puntos < 200:
            nivel_puntos = "medio"
            frases_puntos = [
                "¡Buen esfuerzo, pero puedes dar más! 🚀 Sigue empujando tus límites.",
                "Estás en el camino, ahora a acelerar para alcanzar tus metas. 💥",
                "¡Vas bien, pero el podio está cerca! Sigue entrenando duro. 🏋️"
            ]
        else:
            nivel_puntos = "alto"
            frases_puntos = [
                "¡Eres una máquina! 🔥 Sigue así y nadie te parará.",
                "¡Imparable! Tu esfuerzo está dando frutos, mantén ese ritmo. 💪",
                "¡Crack total! 🏆 Esta semana has demostrado de qué estás hecho."
            ]
        if meta_km == 0:
            km_progreso = "sin_meta"
            frases_km = ["Establece una meta de km para medir tu progreso. ¡Tú puedes! 🏃"]
        elif km_corridos >= meta_km:
            km_progreso = "cumplido"
            frases_km = [
                "¡Meta de km superada! 🏃 Eres un corredor incansable.",
                "¡Kilómetros dominados! 🌟 Sigue corriendo hacia tus sueños.",
                "¡Wow, has volado esta semana! 🚀 Mantén ese ritmo."
            ]
        elif km_corridos >= meta_km * 0.5:
            km_progreso = "mitad"
            frases_km = [
                "¡Más de la mitad del camino recorrido! 🏃 Dale un último empujón.",
                "Estás cerca de la meta de km, ¡no pares ahora! 💨",
                "¡Buen avance en los km! Sigue corriendo y lo lograrás. 🌈"
            ]
        else:
            km_progreso = "bajo"
            frases_km = [
                "Los km están esperando, ¡sal a conquistarlos! 🏃",
                "¡Ánimo con los km! Cada paso te acerca a tu meta. 🌟",
                "No te preocupes, ¡esta semana correrás como el viento! 💨"
            ]
        if nivel_puntos == "bajo" or km_progreso in ["bajo", "sin_meta"]:
            frases = [
                f"{random.choice(frases_puntos)} {random.choice(frases_km)}",
                f"¡Esta semana no fue tu mejor momento, pero eres un luchador! 💪 {random.choice(frases_km)}",
                f"¡Toca darle caña! {random.choice(frases_puntos)} ¡Y a por esos km! 🏃"
            ]
        elif nivel_puntos == "medio" or km_progreso == "mitad":
            frases = [
                f"{random.choice(frases_puntos)} ¡Y con esos km estás cada vez más cerca! 🏃",
                f"¡Gran trabajo, pero puedes brillar más! 🌟 {random.choice(frases_km)}",
                f"{random.choice(frases_puntos)} ¡Un poco más y serás imparable! 💥"
            ]
        else:
            frases = [
                f"{random.choice(frases_puntos)} ¡Y esos km son puro oro! 🏅",
                f"¡Semana épica! {random.choice(frases_puntos)} {random.choice(frases_km)}",
                f"{random.choice(frases_puntos)} ¡Sigue dominando los km como un pro! 🚀"
            ]
        return random.choice(frases)

    def crear_interfaz(self):
        print("Creando interfaz...")
        if not self.modelo.usuarios:
            print("No hay usuarios, inicializando con usuario por defecto.")
            self.modelo.crear_usuario("Usuario")
        header_frame = tk.Frame(self.root, bg="#1e293b", height=50)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        nombre = self.modelo.nombre if self.modelo.nombre else "Usuario"
        tk.Label(header_frame, text=f"Entreno Verano - {nombre}", font=("Arial", 14), fg="white", bg="#1e293b").pack(pady=10)
        style = ttk.Style()
        style.configure("TNotebook", background="#f9fafb")
        style.configure("TNotebook.Tab", font=("Arial", 11), padding=(10, 5), background="#e0f2fe", foreground="black")
        style.map("TNotebook.Tab", background=[("selected", "#ccfbf1")], foreground=[("selected", "black")])
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5, padx=10)
        datos_frame = tk.Frame(notebook, bg="#ffffff")
        notebook.add(datos_frame, text="Datos Personales")
        self.crear_datos_personales(datos_frame)
        entreno_frame = tk.Frame(notebook, bg="#ffffff")
        notebook.add(entreno_frame, text="Entreno Diario")
        self.crear_entreno_diario(entreno_frame)
        correr_frame = tk.Frame(notebook, bg="#ffffff")
        notebook.add(correr_frame, text="Correr")
        self.crear_correr(correr_frame)
        progreso_frame = tk.Frame(notebook, bg="#ffffff")
        notebook.add(progreso_frame, text="Progreso")
        self.crear_progreso(progreso_frame)
        resumen_frame = tk.Frame(notebook, bg="#ffffff")
        notebook.add(resumen_frame, text="Resumen Semanal")
        self.crear_resumen_semanal(resumen_frame)

    def crear_datos_personales(self, frame):
        print("Creando pestaña Datos Personales...")
        panel = tk.Frame(frame, bg="#ffffff")
        panel.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        tk.Label(panel, text="Configura tu Perfil", font=("Arial", 12), bg="#ffffff", fg="#374151").pack(pady=10)
        form_frame = tk.Frame(panel, bg="#ffffff")
        form_frame.pack()
        tk.Label(form_frame, text="Nombre:", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(anchor="w", pady=5)
        self.nombre_combo = ttk.Combobox(form_frame, font=("Arial", 10), width=23, state="normal")
        self.nombre_combo.pack(fill=tk.X, pady=5)
        self.nombre_combo['values'] = list(self.modelo.usuarios.keys())
        if self.modelo.nombre:
            self.nombre_combo.set(self.modelo.nombre)
        else:
            self.nombre_combo.set("")
        self.nombre_combo.bind('<<ComboboxSelected>>', self.cargar_usuario_combo)
        tk.Label(form_frame, text="Peso (kg):", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(anchor="w", pady=5)
        self.entry_peso = tk.Entry(form_frame, font=("Arial", 10), width=25, relief="flat", bg="#f9fafb", bd=1, highlightthickness=1, highlightbackground="#d1d5db")
        self.entry_peso.pack(fill=tk.X, pady=5)
        self.entry_peso.insert(0, str(self.modelo.peso))
        tk.Label(form_frame, text="Estatura (cm):", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(anchor="w", pady=5)
        self.entry_estatura = tk.Entry(form_frame, font=("Arial", 10), width=25, relief="flat", bg="#f9fafb", bd=1, highlightthickness=1, highlightbackground="#d1d5db")
        self.entry_estatura.pack(fill=tk.X, pady=5)
        self.entry_estatura.insert(0, str(self.modelo.estatura))
        tk.Label(form_frame, text="Fecha de inicio (lunes):", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(anchor="w", pady=5)
        self.calendar_semana = DateEntry(form_frame, font=("Arial", 10), date_pattern="dd/mm/yyyy", background="#6ee7b7", foreground="black", width=23)
        self.calendar_semana.pack(fill=tk.X, pady=5)
        self.week_label = tk.Label(form_frame, text="", font=("Arial", 10), bg="#ffffff", fg="#555555")
        self.week_label.pack(anchor="w", pady=5)
        self.calendar_semana.bind("<<DateEntrySelected>>", self.update_week_label)
        tk.Label(form_frame, text="Meta km semanal:", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(anchor="w", pady=5)
        self.entry_km = tk.Entry(form_frame, font=("Arial", 10), width=25, relief="flat", bg="#f9fafb", bd=1, highlightthickness=1, highlightbackground="#d1d5db")
        self.entry_km.pack(fill=tk.X, pady=5)
        self.entry_km.insert(0, "0")
        button_frame = tk.Frame(panel, bg="#ffffff")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Guardar", font=("Arial", 10), bg="#6ee7b7", fg="black", command=self.submit_personal_data, relief="flat").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Nuevo Usuario", font=("Arial", 10), bg="#f44336", fg="white", command=self.crear_nuevo_usuario, relief="flat").pack(side=tk.LEFT, padx=5)
        self.update_week_label()

    def cargar_usuario_combo(self, event=None):
        print("Cargando datos del usuario seleccionado...")
        try:
            nombre = self.nombre_combo.get().strip()
            if nombre:
                self.modelo.cambiar_usuario(nombre)
                self.entry_peso.delete(0, tk.END)
                self.entry_peso.insert(0, str(self.modelo.peso))
                self.entry_estatura.delete(0, tk.END)
                self.entry_estatura.insert(0, str(self.modelo.estatura))
                semana_ano = self.calendar_semana.get_date().isocalendar()[1]
                meta_km = self.modelo.meta_km.get(str(semana_ano), 0) if isinstance(self.modelo.meta_km, dict) else 0
                self.entry_km.delete(0, tk.END)
                self.entry_km.insert(0, str(meta_km))
                for widget in self.root.winfo_children()[0].winfo_children():
                    widget.destroy()
                tk.Label(self.root.winfo_children()[0], text=f"Entreno Verano - {nombre}", font=("Arial", 14), fg="white", bg="#1e293b").pack(pady=10)
                ejercicios_completados = self.modelo.ejercicios_completados
                if not isinstance(ejercicios_completados, dict):
                    print("Inicializando ejercicios_completados como diccionario vacío")
                    ejercicios_completados = {}
                    self.modelo.ejercicios_completados = ejercicios_completados
                self.update_labels()
                self.register_ejercicio()
                self.update_progreso()
            else:
                messagebox.showerror("Error", "Selecciona o escribe un nombre válido")
        except Exception as e:
            print(f"Error en cargar_usuario_combo: {e}")
            messagebox.showerror("Error", f"Error al cargar usuario: {e}")

    def crear_nuevo_usuario(self):
        print("Creando nuevo usuario...")
        try:
            ventana = tk.Toplevel(self.root)
            ventana.title("Nuevo Usuario")
            ventana.geometry("300x150")
            ventana.configure(bg="#ffffff")
            tk.Label(ventana, text="Nombre del nuevo usuario:", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(pady=10)
            entry_nombre = tk.Entry(ventana, font=("Arial", 10), width=25, relief="flat", bg="#f9fafb", bd=1)
            entry_nombre.pack(pady=5)
            def guardar_nuevo_usuario():
                nombre = entry_nombre.get().strip()
                if not nombre:
                    messagebox.showerror("Error", "Ingresa un nombre válido")
                    return
                if nombre in self.modelo.usuarios:
                    messagebox.showerror("Error", "El usuario ya existe")
                    return
                self.modelo.crear_usuario(nombre)
                self.nombre_combo['values'] = list(self.modelo.usuarios.keys())
                self.nombre_combo.set(nombre)
                self.modelo.cambiar_usuario(nombre)
                self.entry_peso.delete(0, tk.END)
                self.entry_peso.insert(0, "0")
                self.entry_estatura.delete(0, tk.END)
                self.entry_estatura.insert(0, "0")
                self.entry_km.delete(0, tk.END)
                self.entry_km.insert(0, "0")
                self.modelo.ejercicios_completados = {}
                self.modelo.ejercicios_personalizados = {}
                self.modelo.guardar_datos()
                for widget in self.root.winfo_children()[0].winfo_children():
                    widget.destroy()
                tk.Label(self.root.winfo_children()[0], text=f"Entreno Verano - {nombre}", font=("Arial", 14), fg="white", bg="#1e293b").pack(pady=10)
                self.update_labels()
                self.update_progreso()
                self.register_ejercicio()
                messagebox.showinfo("Éxito", f"Usuario '{nombre}' creado")
                ventana.destroy()
            tk.Button(ventana, text="Crear", font=("Arial", 10), bg="#6ee7b7", fg="black", command=guardar_nuevo_usuario, relief="flat").pack(pady=10)
            tk.Button(ventana, text="Cancelar", font=("Arial", 10), bg="#f3f4f6", fg="black", command=ventana.destroy, relief="flat").pack(pady=5)
        except Exception as e:
            print(f"Error en crear_nuevo_usuario: {e}")
            messagebox.showerror("Error", f"Error al crear usuario: {e}")

    def submit_personal_data(self):
        print("Guardando datos personales...")
        try:
            nombre = self.nombre_combo.get().strip()
            peso = float(self.entry_peso.get())
            estatura = float(self.entry_estatura.get())
            fecha = self.calendar_semana.get_date()
            semana_ano = fecha.isocalendar()[1]
            km = float(self.entry_km.get())
            if not nombre:
                messagebox.showerror("Error", "El nombre no puede estar vacío")
                return
            if peso <= 0 or estatura < 100 or km < 0:
                messagebox.showerror("Error", "Peso > 0, estatura > 100 cm, km >= 0")
                return
            self.modelo.crear_usuario(nombre)
            self.modelo.nombre = nombre
            self.modelo.peso = peso
            self.modelo.estatura = estatura
            if not isinstance(self.modelo.meta_km, dict):
                self.modelo.meta_km = {}
            self.modelo.meta_km[str(semana_ano)] = km
            self.modelo.guardar_datos()
            self.nombre_combo['values'] = list(self.modelo.usuarios.keys())
            messagebox.showinfo("Éxito", "Datos guardados correctamente")
            for widget in self.root.winfo_children()[0].winfo_children():
                widget.destroy()
            tk.Label(self.root.winfo_children()[0], text=f"Entreno Verano - {nombre}", font=("Arial", 14), fg="white", bg="#1e293b").pack(pady=10)
            self.update_labels()
            self.update_progreso()
        except ValueError:
            messagebox.showerror("Error", "Ingresa valores numéricos válidos")
        except Exception as e:
            print(f"Error en submit_personal_data: {e}")
            messagebox.showerror("Error", f"Error al guardar datos: {e}")

    def update_week_label(self, event=None):
        if self.sincronizando:
            print("Evitando sincronización recursiva en update_week_label...")
            return
        print("Actualizando etiqueta de semana...")
        try:
            fecha = self.calendar_semana.get_date()
            if not fecha:
                raise ValueError("Fecha no válida")
            dia_semana = fecha.weekday()
            lunes = fecha - timedelta(days=dia_semana)
            domingo = lunes + timedelta(days=6)
            self.week_label.config(text=f"Semana: {lunes.strftime('%d/%m/%Y')} - {domingo.strftime('%d/%m/%Y')}")
            semana_ano = fecha.isocalendar()[1]
            self.selected_week = (semana_ano, fecha.year)
            meta_km = self.modelo.meta_km.get(str(semana_ano), 0) if isinstance(self.modelo.meta_km, dict) else 0
            self.entry_km.delete(0, tk.END)
            self.entry_km.insert(0, str(meta_km))
            self.sincronizar_calendarios(fecha)
        except Exception as e:
            print(f"Error en update_week_label: {e}")
            messagebox.showerror("Error", f"Error al actualizar semana: {e}")

    def sincronizar_calendarios(self, fecha):
        if self.sincronizando:
            print("Evitando sincronización recursiva...")
            return
        self.sincronizando = True
        print(f"Sincronizando calendarios para fecha: {fecha}")
        try:
            dia_semana = fecha.weekday()
            lunes = fecha - timedelta(days=dia_semana)
            if hasattr(self, 'calendar') and self.calendar:
                self.calendar.set_date(fecha)
                self.update_entreno()
            if hasattr(self, 'correr_calendar') and self.correr_calendar:
                self.correr_calendar.set_date(fecha)
                self.update_correr()
            if hasattr(self, 'calendar_resumen') and self.calendar_resumen:
                self.calendar_resumen.set_date(fecha)
                self.update_labels()
            if hasattr(self, 'calendar_semana') and self.calendar_semana:
                self.calendar_semana.set_date(lunes)
        except Exception as e:
            print(f"Error al sincronizar calendarios: {e}")
            messagebox.showerror("Error", f"Error al sincronizar calendarios: {e}")
        finally:
            self.sincronizando = False

    def anadir_ejercicio_personalizado(self):
        print("Añadiendo ejercicio personalizado...")
        try:
            fecha = self.calendar.get_date()
            if not fecha:
                raise ValueError("Fecha no válida")
            fecha_str = fecha.strftime("%Y-%m-%d")
            ventana = tk.Toplevel(self.root)
            ventana.title("Añadir Ejercicio Personalizado")
            ventana.geometry("400x200")
            ventana.configure(bg="#ffffff")
            tk.Label(ventana, text="Nombre del ejercicio:", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(pady=10)
            entry_ejercicio = tk.Entry(ventana, font=("Arial", 10), width=30, relief="flat", bg="#f9fafb", bd=1)
            entry_ejercicio.pack(pady=5)
            def guardar_ejercicio():
                nombre_ejercicio = entry_ejercicio.get().strip()
                try:
                    if not nombre_ejercicio:
                        messagebox.showerror("Error", "Ingresa un nombre válido para el ejercicio")
                        return
                    ejercicios_personalizados = self.modelo.ejercicios_personalizados
                    if not isinstance(ejercicios_personalizados, dict):
                        ejercicios_personalizados = {}
                    if fecha_str not in ejercicios_personalizados:
                        ejercicios_personalizados[fecha_str] = []
                    ejercicios_personalizados[fecha_str].append(nombre_ejercicio)
                    self.modelo.ejercicios_personalizados = ejercicios_personalizados
                    self.modelo.guardar_datos()
                    messagebox.showinfo("Éxito", f"Ejercicio '{nombre_ejercicio}' añadido para {fecha_str}")
                    ventana.destroy()
                    self.register_ejercicio()
                except Exception as e:
                    print(f"Error al guardar ejercicio: {e}")
                    messagebox.showerror("Error", f"Error al guardar ejercicio: {e}")
            tk.Button(ventana, text="Guardar", font=("Arial", 10), bg="#6ee7b7", fg="black", command=guardar_ejercicio, relief="flat").pack(pady=10)
            tk.Button(ventana, text="Cancelar", font=("Arial", 10), bg="#f3f4f6", fg="black", command=ventana.destroy, relief="flat").pack(pady=5)
        except Exception as e:
            print(f"Error en anadir_ejercicio_personalizado: {e}")
            messagebox.showerror("Error", f"Error al añadir ejercicio: {e}")

    def crear_entreno_diario(self, frame):
        print("Creando pestaña Entreno Diario...")
        panel = tk.Frame(frame, bg="#ffffff")
        panel.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        tk.Label(panel, text="Selecciona fecha:", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(anchor="w", pady=5)
        self.calendar = DateEntry(panel, font=("Arial", 10), date_pattern="dd/mm/yyyy", background="#6ee7b7", foreground="black", width=23)
        self.calendar.pack(anchor="w", pady=5)
        self.calendar.bind("<<DateEntrySelected>>", self.update_entreno_calendar)
        button_frame = tk.Frame(panel, bg="#ffffff")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Mostrar Ejercicios", font=("Arial", 10), bg="#6ee7b7", fg="black", command=self.register_ejercicio, relief="flat").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Añadir Ejercicio", font=("Arial", 10), bg="#ff9800", fg="black", command=self.anadir_ejercicio_personalizado, relief="flat").pack(side=tk.LEFT, padx=5)
        self.progress_label = tk.Label(panel, text="Puntos del día: 0", font=("Arial", 10), bg="#ffffff", fg="#333333")
        self.progress_label.pack(anchor="w", pady=5)
        self.frase_diaria_label = tk.Label(panel, text="", font=("Arial", 10, "italic"), bg="#ffffff", fg="#555555", wraplength=500)
        self.frase_diaria_label.pack(anchor="w", pady=5)
        self.progress_bar = ttk.Progressbar(panel, orient="horizontal", length=150, mode="determinate")
        self.progress_bar.pack(anchor="w", pady=5)
        canvas = tk.Canvas(panel, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(panel, orient="vertical", command=canvas.yview)
        self.exercise_frame = tk.Frame(canvas, bg="#ffffff")
        self.exercise_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.exercise_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.update_entreno()

    def update_entreno_calendar(self, event=None):
        if self.sincronizando:
            print("Evitando actualización recursiva...")
            return
        print("Actualizando calendario de Entreno Diario...")
        try:
            fecha = self.calendar.get_date()
            if not fecha:
                raise ValueError("Fecha no válida")
            semana_ano = fecha.isocalendar()[1]
            ano = fecha.year
            self.selected_week = (semana_ano, ano)
            print(f"Fecha seleccionada: {fecha}, Semana: {semana_ano}, Año: {ano}")
            self.sincronizar_calendarios(fecha)
            self.update_entreno()
        except Exception as e:
            print(f"Error en update_entreno_calendar: {e}")
            messagebox.showerror("Error", f"Error al actualizar calendario: {e}")

    def update_entreno(self):
        print("Actualizando pestaña Entreno Diario...")
        try:
            self.register_ejercicio()
        except Exception as e:
            print(f"Error en update_entreno: {e}")
            tk.Label(self.exercise_frame, text="Error al actualizar ejercicios.", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(anchor="w", pady=10)

    def register_ejercicio(self):
        print("Registrando ejercicios...")
        for widget in self.exercise_frame.winfo_children():
            widget.destroy()
        try:
            fecha = self.calendar.get_date()
            if not fecha:
                raise ValueError("Fecha no válida")
            if fecha > datetime.now().date():
                tk.Label(self.exercise_frame, text="No se pueden registrar ejercicios futuros.", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(anchor="w", pady=5)
                return
            fecha_str = fecha.strftime("%Y-%m-%d")
            ejercicios = self.ejercicios.get_ejercicios_dia(fecha) or []
            print(f"Ejercicios predefinidos para {fecha_str}: {ejercicios}")
            ejercicios_personalizados = self.modelo.ejercicios_personalizados.get(fecha_str, []) if isinstance(self.modelo.ejercicios_personalizados, dict) else []
            print(f"Ejercicios personalizados para {fecha_str}: {ejercicios_personalizados}")
            todos_ejercicios = ejercicios + ejercicios_personalizados
            if not todos_ejercicios:
                print(f"Advertencia: No se encontraron ejercicios para {fecha_str}")
                tk.Label(self.exercise_frame, text="No hay ejercicios disponibles para este día.", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(anchor="w", pady=10)
                return
            ejercicios_completados = self.modelo.ejercicios_completados
            if not isinstance(ejercicios_completados, dict):
                print("Inicializando ejercicios_completados como diccionario vacío")
                ejercicios_completados = {}
                self.modelo.ejercicios_completados = ejercicios_completados
            if fecha_str not in ejercicios_completados:
                ejercicios_completados[fecha_str] = {}
            for ejercicio in todos_ejercicios:
                ejercicios_completados[fecha_str].setdefault(ejercicio, False)
            self.modelo.ejercicios_completados = ejercicios_completados
            self.modelo.guardar_datos()
            self.check_vars = []
            for ejercicio in todos_ejercicios:
                frame = tk.Frame(self.exercise_frame, bg="#ffffff")
                frame.pack(anchor="w", pady=5)
                completado = ejercicios_completados[fecha_str].get(ejercicio, False)
                var = tk.BooleanVar(value=completado)
                self.check_vars.append((ejercicio, var))
                chk = tk.Checkbutton(
                    frame,
                    text=f"{ejercicio} ({self.ejercicios.get_puntos(ejercicio)} puntos)",
                    font=("Arial", 10),
                    bg="#ffffff",
                    fg="#333333",
                    variable=var,
                    command=lambda ej=ejercicio: self.toggle_ejercicio(ej, fecha_str)
                )
                chk.pack(side=tk.LEFT)
            puntos_dia = sum(
                self.ejercicios.get_puntos(ejercicio)
                for ejercicio, completado in ejercicios_completados[fecha_str].items()
                if completado
            )
            max_puntos = sum(self.ejercicios.get_puntos(ejercicio) for ejercicio in todos_ejercicios)
            self.progress_label.config(text=f"Puntos del día: {puntos_dia}")
            self.frase_diaria_label.config(text=self.get_frase_diaria(puntos_dia))
            self.progress_bar['value'] = (puntos_dia / max_puntos * 100) if max_puntos > 0 else 0
        except Exception as e:
            print(f"Error en register_ejercicio: {e}")
            messagebox.showerror("Error", f"Error al cargar ejercicios: {e}")

    def toggle_ejercicio(self, ejercicio, fecha_str):
        print(f"Actualizando estado de ejercicio: {ejercicio}")
        try:
            ejercicios_completados = self.modelo.ejercicios_completados
            if not isinstance(ejercicios_completados, dict):
                ejercicios_completados = {}
                self.modelo.ejercicios_completados = ejercicios_completados
            if fecha_str not in ejercicios_completados:
                ejercicios_completados[fecha_str] = {}
            for ej, var in self.check_vars:
                if ej == ejercicio:
                    ejercicios_completados[fecha_str][ejercicio] = var.get()
                    break
            self.modelo.ejercicios_completados = ejercicios_completados
            self.modelo.guardar_datos()
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            semana_ano = fecha.isocalendar()[1]
            ano = fecha.year
            puntos_semana = 0
            completados = 0
            total_ejercicios = 0
            lunes = fecha - timedelta(days=fecha.weekday())
            for i in range(7):
                dia = lunes + timedelta(days=i)
                dia_str = dia.strftime("%Y-%m-%d")
                ejercicios_dia = self.ejercicios.get_ejercicios_dia(dia) + self.modelo.ejercicios_personalizados.get(dia_str, [])
                total_ejercicios += len(ejercicios_dia)
                for ej in ejercicios_dia:
                    if ejercicios_completados.get(dia_str, {}).get(ej, False):
                        puntos_semana += self.ejercicios.get_puntos(ej)
                        completados += 1
            for item in self.modelo.historial_semanal:
                if item["semana"] == semana_ano and item.get("año", ano) == ano:
                    item["puntos"] = puntos_semana
                    item["completados"] = completados / total_ejercicios if total_ejercicios > 0 else 0
                    break
            else:
                self.modelo.historial_semanal.append({
                    "semana": semana_ano,
                    "puntos": puntos_semana,
                    "km": 0.0,
                    "completados": completados / total_ejercicios if total_ejercicios > 0 else 0,
                    "recompensa": "",
                    "recompensa_texto": "",
                    "año": ano
                })
            self.modelo.guardar_datos()
            todos_ejercicios = self.ejercicios.get_ejercicios_dia(fecha) + self.modelo.ejercicios_personalizados.get(fecha_str, [])
            puntos_dia = sum(
                self.ejercicios.get_puntos(ej)
                for ej in todos_ejercicios
                if ejercicios_completados.get(fecha_str, {}).get(ej, False)
            )
            max_puntos = sum(self.ejercicios.get_puntos(ej) for ej in todos_ejercicios)
            self.progress_label.config(text=f"Puntos del día: {puntos_dia}")
            self.frase_diaria_label.config(text=self.get_frase_diaria(puntos_dia))
            self.progress_bar['value'] = (puntos_dia / max_puntos * 100) if max_puntos > 0 else 0
            self.update_labels()
            self.update_progreso()
        except Exception as e:
            print(f"Error en toggle_ejercicio: {e}")
            messagebox.showerror("Error", f"Error al actualizar ejercicio: {e}")

    def crear_correr(self, frame):
        print("Creando pestaña Correr...")
        panel = tk.Frame(frame, bg="#ffffff")
        panel.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        tk.Label(panel, text="Correr", font=("Arial", 12), bg="#ffffff", fg="#333333").pack(pady=10)
        tk.Label(panel, text="Selecciona fecha:", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(anchor="w", pady=5)
        self.correr_calendar = DateEntry(panel, font=("Arial", 10), date_pattern="dd/mm/yyyy", background="#6ee7b7", foreground="black", width=23)
        self.correr_calendar.pack(anchor="w", pady=5)
        self.correr_calendar.bind("<<DateEntrySelected>>", self.update_correr_calendar)
        km_frame = tk.Frame(panel, bg="#f9fafb", bd=1, relief="flat")
        km_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(km_frame, text="Kilómetros diarios:", font=("Arial", 10), bg="#f9fafb", fg="#333333").pack(anchor="w", pady=5)
        self.km_entry = tk.Entry(km_frame, font=("Arial", 10), width=8, relief="flat", bg="#ffffff", bd=1)
        self.km_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(km_frame, text="Registrar", font=("Arial", 10), bg="#6ee7b7", fg="black", command=self.register_km, relief="flat").pack(side=tk.LEFT, padx=5)
        columns = ("Fecha", "Kilómetros")
        self.km_tree = ttk.Treeview(panel, columns=columns, show="headings", height=7)
        self.km_tree.heading("Fecha", text="Fecha")
        self.km_tree.heading("Kilómetros", text="Km")
        self.km_tree.column("Fecha", width=150, anchor="center")
        self.km_tree.column("Kilómetros", width=100, anchor="center")
        self.km_tree.pack(fill=tk.X, pady=10, padx=10)
        tk.Button(panel, text="Ver Gráficas", font=("Arial", 10), bg="#ff9800", fg="black", command=self.mostrar_graficas_correr, relief="flat").pack(pady=10)
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.update_correr()

    def update_correr_calendar(self, event=None):
        if self.sincronizando:
            print("Evitando actualización recursiva...")
            return
        print("Actualizando calendario de Correr...")
        try:
            fecha = self.correr_calendar.get_date()
            if not fecha:
                raise ValueError("Fecha no válida")
            semana_ano = fecha.isocalendar()[1]
            ano = fecha.year
            self.selected_week = (semana_ano, ano)
            self.sincronizar_calendarios(fecha)
            self.update_correr()
        except Exception as e:
            print(f"Error en update_correr_calendar: {e}")
            messagebox.showerror("Error", f"Error al actualizar calendario: {e}")

    def update_correr(self):
        print("Actualizando pestaña Correr...")
        try:
            for widget in self.km_tree.master.winfo_children():
                if isinstance(widget, tk.Label) and ("Error" in widget.cget("text") or "Semana futura" in widget.cget("text")):
                    widget.destroy()
            for item in self.km_tree.get_children():
                self.km_tree.delete(item)
            fecha = self.correr_calendar.get_date()
            dia_semana = fecha.weekday()
            lunes = fecha - timedelta(days=dia_semana)
            semana_ano = lunes.isocalendar()[1]
            ano = fecha.year
            current_week = datetime.now().isocalendar()[1]
            current_year = datetime.now().year
            if ano > current_year or (ano == current_year and semana_ano > current_week):
                tk.Label(self.km_tree.master, text="Semana futura no disponible.", font=("Arial", 10), bg="#ffffff", fg="red").pack(anchor="w", pady=10)
                return
            km_corridos = self.modelo.km_corridos if isinstance(self.modelo.km_corridos, dict) else {}
            for i in range(7):
                dia = lunes + timedelta(days=i)
                dia_str = dia.strftime("%Y-%m-%d")
                km = km_corridos.get(dia_str, 0.0)
                self.km_tree.insert("", tk.END, values=(dia.strftime("%d/%m/%Y"), f"{km:.2f}"))
            self.km_tree.yview_moveto(0)
        except Exception as e:
            print(f"Error en update_correr: {e}")
            tk.Label(self.km_tree.master, text="Error al actualizar datos.", font=("Arial", 10), bg="#ffffff", fg="red").pack(anchor="w", pady=10)

    def register_km(self):
        print("Registrando kilómetros...")
        try:
            km = float(self.km_entry.get())
            if km < 0:
                messagebox.showerror("Error", "Ingresa un número >= 0")
                return
            fecha = self.correr_calendar.get_date()
            if fecha > datetime.now().date():
                messagebox.showerror("Error", "No se pueden registrar kilómetros futuros")
                return
            fecha_str = fecha.strftime("%Y-%m-%d")
            if not isinstance(self.modelo.km_corridos, dict):
                self.modelo.km_corridos = {}
            self.modelo.km_corridos[fecha_str] = self.modelo.km_corridos.get(fecha_str, 0.0) + km
            semana_ano = fecha.isocalendar()[1]
            ano = fecha.year
            km_semana = 0.0
            lunes = fecha - timedelta(days=fecha.weekday())
            for i in range(7):
                dia = lunes + timedelta(days=i)
                dia_str = dia.strftime("%Y-%m-%d")
                km_semana += self.modelo.km_corridos.get(dia_str, 0.0)
            for item in self.modelo.historial_semanal:
                if item["semana"] == semana_ano and item.get("año", ano) == ano:
                    item["km"] = km_semana
                    break
            else:
                self.modelo.historial_semanal.append({
                    "semana": semana_ano,
                    "puntos": 0,
                    "km": km_semana,
                    "completados": 0,
                    "recompensa": "",
                    "recompensa_texto": "",
                    "año": ano
                })
            self.modelo.guardar_datos()
            self.km_entry.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Kilometraje registrado")
            self.update_correr()
            self.update_labels()
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número válido")
        except Exception as e:
            print(f"Error en register_km: {e}")
            messagebox.showerror("Error", f"Error al registrar: {e}")

    def mostrar_graficas_correr(self):
        print("Mostrando gráficas de Correr...")
        window = tk.Toplevel(self.root)
        window.title("Gráfica de Correr")
        window.geometry("600x400")
        window.configure(bg="#ffffff")
        try:
            current_week = datetime.now().isocalendar()[1]
            current_year = datetime.now().year
            historial_filtrado = [
                item for item in self.modelo.historial_semanal
                if item.get("año", current_year) <= current_year and item["semana"] <= current_week
            ]
            if not historial_filtrado:
                tk.Label(window, text="No hay datos.", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(pady=20)
                return
            historial_ordenado = sorted(historial_filtrado, key=lambda x: (x.get("año", current_year), x["semana"]))[-10:]
            semanas = [item["semana"] for item in historial_ordenado]
            km = [item["km"] for item in historial_ordenado]
            fechas = [
                f"{self.get_week_dates(semana, item.get('año', current_year))[0]}-{self.get_week_dates(semana, item.get('año', current_year))[1]}"
                for item, semana in zip(historial_ordenado, semanas)
            ]
            step = 3 if len(semanas) > 5 else 1
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(range(len(semanas)), km, color="#ff9800", edgecolor="black", alpha=0.8)
            ax.set_title("Kilómetros por Semana", fontsize=10, fontweight="bold")
            ax.set_xlabel("Semana", fontsize=8)
            ax.set_ylabel("Kilometraje", fontsize=8)
            ax.set_xticks(range(0, len(semanas), step))
            ax.set_xticklabels([fechas[i] for i in range(0, len(semanas), step)], rotation=45, fontsize=7)
            ax.grid(True, axis="y", linestyle="--", alpha=0.7, color="#d3d3d3")
            for i, v in enumerate(km):
                ax.text(i, v + 0.5, f"{v:.1f}", fontsize=8, ha="center", va="bottom")
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            window.protocol("WM_DELETE_WINDOW", lambda: [plt.close(fig), window.destroy()])
        except Exception as e:
            print(f"Error en mostrar_graficas_correr: {e}")
            tk.Label(window, text="Error al generar gráfica.", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(pady=20)

    def crear_progreso(self, frame):
        print("Creando pestaña Progreso...")
        panel = tk.Frame(frame, bg="#ffffff")
        panel.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        tk.Label(panel, text="Progresión Semanal", font=("Arial", 12), bg="#ffffff", fg="#000000").pack(pady=10)
        columns = ("Semana", "Puntos", "Completados")
        self.tree = ttk.Treeview(panel, columns=columns, show="headings", height=10)
        self.tree.heading("Semana", text="Semana")
        self.tree.heading("Puntos", text="Puntos")
        self.tree.heading("Completados", text="% Completados")
        self.tree.column("Semana", width=100, anchor="center")
        self.tree.column("Puntos", width=100, anchor="center")
        self.tree.column("Completados", width=100, anchor="center")
        self.tree.pack(pady=10, padx=10)
        tk.Button(panel, text="Ver Gráficas", font=("Arial", 10), bg="#ff9800", fg="black", command=self.mostrar_graficas_progreso, relief="flat").pack(pady=10)
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.update_progreso()

    def update_progreso(self):
        print("Actualizando progreso...")
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            current_week = datetime.now().isocalendar()[1]
            current_year = datetime.now().year
            for item in sorted(self.modelo.historial_semanal, key=lambda x: (x.get("año", current_year), x["semana"]))[-10:]:
                if item.get("año", current_year) <= current_year and item["semana"] <= current_week:
                    semana_ano = item["semana"]
                    ano = item.get("año", current_year)
                    puntos = 0
                    completados = 0
                    total_ejercicios = 0
                    lunes = datetime.strptime(f"{ano}-W{int(semana_ano)-1}-1", "%Y-W%W-%w").date()
                    for i in range(7):
                        dia = lunes + timedelta(days=i)
                        dia_str = dia.strftime("%Y-%m-%d")
                        ejercicios_dia = self.ejercicios.get_ejercicios_dia(dia) + self.modelo.ejercicios_personalizados.get(dia_str, [])
                        total_ejercicios += len(ejercicios_dia)
                        for ej in ejercicios_dia:
                            if self.modelo.ejercicios_completados.get(dia_str, {}).get(ej, False):
                                completados += 1
                                puntos += self.ejercicios.get_puntos(ej)
                    porcentaje = (completados / total_ejercicios * 100) if total_ejercicios > 0 else 0
                    self.tree.insert("", tk.END, values=(f"{semana_ano}", puntos, f"{porcentaje:.1f}%"))
        except Exception as e:
            print(f"Error en update_progreso: {e}")
            tk.Label(self.tree.master, text="Error al actualizar datos.", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(anchor="w", pady=10)

    def mostrar_graficas_progreso(self):
        print("Mostrando gráficas de Progreso...")
        window = tk.Toplevel(self.root)
        window.title("Gráficas de Progreso")
        window.geometry("800x600")
        window.configure(bg="#ffffff")
        try:
            current_week = datetime.now().isocalendar()[1]
            current_year = datetime.now().year
            historial_filtrado = [
                item for item in self.modelo.historial_semanal
                if item.get("año", current_year) <= current_year and item["semana"] <= current_week
            ]
            if not historial_filtrado:
                tk.Label(window, text="No hay datos disponibles.", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(pady=20)
                return
            historial_ordenado = sorted(historial_filtrado, key=lambda x: (x.get("año", current_year), x["semana"]))[-10:]
            semanas = [item["semana"] for item in historial_ordenado]
            puntos = []
            porcentajes = []
            for item in historial_ordenado:
                semana_ano = item["semana"]
                ano = item.get("año", current_year)
                puntos_total = 0
                completados_total = 0
                total_ejercicios = 0
                lunes = datetime.strptime(f"{ano}-W{int(semana_ano)-1}-1", "%Y-W%W-%w").date()
                for i in range(7):
                    dia = lunes + timedelta(days=i)
                    dia_str = dia.strftime("%Y-%m-%d")
                    ejercicios_dia = self.ejercicios.get_ejercicios_dia(dia) + self.modelo.ejercicios_personalizados.get(dia_str, [])
                    total_ejercicios += len(ejercicios_dia)
                    for ej in ejercicios_dia:
                        if self.modelo.ejercicios_completados.get(dia_str, {}).get(ej, False):
                            completados_total += 1
                            puntos_total += self.ejercicios.get_puntos(ej)
                puntos.append(puntos_total)
                porcentajes.append((completados_total / total_ejercicios * 100) if total_ejercicios > 0 else 0)
            fechas = [
                f"{self.get_week_dates(semana, item.get('año', current_year))[0]}-{self.get_week_dates(semana, item.get('año', current_year))[1]}"
                for item, semana in zip(historial_ordenado, semanas)
            ]
            step = 3 if len(semanas) > 5 else 1
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
            ax1.bar(range(len(semanas)), puntos, color="#6ee7b7", edgecolor="black", alpha=0.8)
            ax1.set_title("Puntos por Semana", fontsize=10, fontweight="bold")
            ax1.set_xlabel("Semana", fontsize=8)
            ax1.set_ylabel("Puntos", fontsize=8)
            ax1.set_xticks(range(0, len(semanas), step))
            ax1.set_xticklabels([fechas[i] for i in range(0, len(semanas), step)], rotation=45, fontsize=7)
            ax1.grid(True, axis="y", linestyle="--", alpha=0.7, color="#d3d3d3")
            for i, v in enumerate(puntos):
                ax1.text(i, v + 1, f"{v}", fontsize=8, ha="center", va="bottom")
            ax2.bar(range(len(semanas)), porcentajes, color="#ff9800", edgecolor="black", alpha=0.8)
            ax2.set_title("Porcentaje de Ejercicios Completados por Semana", fontsize=10, fontweight="bold")
            ax2.set_xlabel("Semana", fontsize=8)
            ax2.set_ylabel("% Completados", fontsize=8)
            ax2.set_xticks(range(0, len(semanas), step))
            ax2.set_xticklabels([fechas[i] for i in range(0, len(semanas), step)], rotation=45, fontsize=7)
            ax2.grid(True, axis="y", linestyle="--", alpha=0.7, color="#d3d3d3")
            for i, v in enumerate(porcentajes):
                ax2.text(i, v + 1, f"{v:.1f}%", fontsize=8, ha="center", va="bottom")
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            window.protocol("WM_DELETE_WINDOW", lambda: [plt.close(fig), window.destroy()])
        except Exception as e:
            print(f"Error en mostrar_graficas_progreso: {e}")
            tk.Label(window, text="Error al generar gráficas.", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(pady=20)

    def crear_resumen_semanal(self, frame):
        print("Creando pestaña Resumen Semanal...")
        panel = tk.Frame(frame, bg="#ffffff")
        panel.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        tk.Label(panel, text="Resumen Semanal", font=("Arial", 12), bg="#ffffff", fg="#333333").pack(pady=10)
        tk.Label(panel, text="Selecciona una fecha de la semana:", font=("Arial", 10), bg="#ffffff", fg="#333333").pack(anchor="w", pady=5)
        self.calendar_resumen = DateEntry(panel, font=("Arial", 10), date_pattern="dd/mm/yyyy", background="#6ee7b7", foreground="black", width=23)
        self.calendar_resumen.pack(anchor="w", pady=5)
        self.calendar_resumen.bind("<<DateEntrySelected>>", self.update_resumen_calendar)
        tk.Button(panel, text="Confirmar Semana", font=("Arial", 12), bg="#6ee7b7", fg="black", command=self.mostrar_resumen, relief="flat").pack(pady=10)
        self.resumen_texto = tk.Label(panel, text="", font=("Arial", 12), bg="#ffffff", fg="#333333", wraplength=500, justify="center")
        self.resumen_texto.pack(pady=10)
        self.imagen_recompensa_label = tk.Label(panel, bg="#ffffff")
        self.imagen_recompensa_label.pack(pady=10)
        self.update_labels()

    def update_resumen_calendar(self, event=None):
        if self.sincronizando:
            print("Evitando actualización recursiva...")
            return
        try:
            fecha = self.calendar_resumen.get_date()
            if not fecha:
                raise ValueError("Fecha no válida")
            semana_ano = fecha.isocalendar()[1]
            ano = fecha.year
            self.selected_week = (semana_ano, ano)
            self.sincronizar_calendarios(fecha)
            self.update_labels()
        except Exception as e:
            print(f"Error en update_resumen_calendar: {e}")
            messagebox.showerror("Error", f"Error al actualizar calendario: {e}")

    def mostrar_resumen(self):
        print("Mostrando resumen semanal...")
        try:
            fecha = self.calendar_resumen.get_date()
            semana_ano = fecha.isocalendar()[1]
            ano = fecha.year
            resultado = self.modelo.evaluar_semana(self.ejercicios.get_ejercicios_dia, fecha, self.ejercicios.get_puntos)
            if isinstance(resultado, str):
                messagebox.showerror("Error", resultado)
                return
            puntos, km_total, completados_total, recompensa, mensaje = resultado
            meta_km = self.modelo.meta_km.get(str(semana_ano), 0) if isinstance(self.modelo.meta_km, dict) else 0
            frase = self.get_frase_semanal(puntos, km_total, meta_km, completados_total)
            texto_resumen = (
                f"Semana {semana_ano} - Puntos: {puntos}\n"
                f"Ejercicios completados: {completados_total}\n"
                f"Kilómetros: {km_total:.2f} / {meta_km:.1f}\n"
                f"Recompensa: {recompensa}\n\n"
                f"{mensaje}\n\n{frase}"
            )
            self.resumen_texto.config(text=texto_resumen)
            photo, img_path = self.generar_imagen_recompensa(recompensa)
            if photo:
                self.imagen_recompensa_label.config(image=photo)
                self.imagen_recompensa_label.image = photo
                if img_path and os.path.exists(img_path):
                    os.remove(img_path)
        except Exception as e:
            print(f"Error en mostrar_resumen: {e}")
            messagebox.showerror("Error", f"Error al mostrar resumen: {e}")

    def update_labels(self):
        print("Actualizando labels de resumen...")
        try:
            if hasattr(self, 'resumen_texto'):
                self.resumen_texto.config(text="")
            if hasattr(self, 'imagen_recompensa_label'):
                self.imagen_recompensa_label.config(image="")
        except Exception as e:
            print(f"Error en update_labels: {e}")
            messagebox.showerror("Error", f"Error al actualizar labels: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    modelo = Modelo()
    ejercicios = Ejercicios()
    app = Interfaz(root, modelo, ejercicios)
    root.mainloop()