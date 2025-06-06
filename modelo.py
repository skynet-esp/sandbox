import json
import os
from datetime import datetime, timedelta

class Modelo:
    def __init__(self):
        print("Inicializando Modelo...")
        self.usuarios = {}
        self.usuario_actual = None
        self.cargar_datos()

    def cargar_datos(self):
        print("Cargando datos desde entreno_verano.json...")
        try:
            if os.path.exists("entreno_verano.json"):
                with open("entreno_verano.json", "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    if isinstance(datos, dict):
                        if "usuarios" in datos and isinstance(datos["usuarios"], dict):
                            self.usuarios = datos["usuarios"]
                            self.usuario_actual = datos.get("usuario_actual", None)
                            if self.usuario_actual and self.usuario_actual in self.usuarios:
                                print(f"Usuario actual cargado: {self.usuario_actual}")
                            else:
                                self.usuario_actual = None
                        else:
                            print("Estructura antigua detectada, migrando datos...")
                            self.usuarios = {
                                datos.get("nombre", "Usuario"): {
                                    "nombre": datos.get("nombre", "Usuario"),
                                    "peso": datos.get("peso", 0.0),
                                    "estatura": datos.get("estatura", 0.0),
                                    "meta_km": datos.get("meta_km", {}),
                                    "km_corridos": datos.get("km_corridos", {}),
                                    "ejercicios_completados": datos.get("ejercicios_completados", {}),
                                    "historial_semanal": datos.get("historial_semanal", []),
                                    "mensaje": datos.get("mensaje", ""),
                                    "ejercicios_personalizados": datos.get("ejercicios_personalizados", {})
                                }
                            }
                            self.usuario_actual = datos.get("nombre", "Usuario")
                            self.guardar_datos()
            else:
                print("Archivo no encontrado, inicializando datos vacíos.")
                self.crear_usuario("Usuario")
        except Exception as e:
            print(f"Error al cargar datos: {e}")

    def guardar_datos(self):
        print("Guardando datos en entreno_verano.json...")
        try:
            datos = {
                "usuarios": self.usuarios,
                "usuario_actual": self.usuario_actual
            }
            with open("entreno_verano.json", "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar datos: {e}")

    def crear_usuario(self, nombre):
        print(f"Creando usuario: {nombre}")
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        if nombre in self.usuarios:
            print(f"Usuario {nombre} ya existe, seleccionándolo.")
            self.cambiar_usuario(nombre)
        else:
            self.usuarios[nombre] = {
                "nombre": nombre,
                "peso": 0.0,
                "estatura": 0.0,
                "meta_km": {},
                "km_corridos": {},
                "ejercicios_completados": {},
                "historial_semanal": [],
                "mensaje": "",
                "ejercicios_personalizados": {}
            }
            self.usuario_actual = nombre
        self.guardar_datos()

    def cambiar_usuario(self, nombre):
        print(f"Cambiando a usuario: {nombre}")
        if nombre in self.usuarios:
            self.usuario_actual = nombre
            self.guardar_datos()
        else:
            raise ValueError(f"Usuario {nombre} no existe")

    @property
    def nombre(self):
        return self.usuarios[self.usuario_actual]["nombre"] if self.usuario_actual else ""

    @nombre.setter
    def nombre(self, value):
        if self.usuario_actual:
            if not value:
                raise ValueError("El nombre no puede estar vacío")
            old_nombre = self.usuarios[self.usuario_actual]["nombre"]
            if old_nombre != value:
                self.usuarios[value] = self.usuarios.pop(old_nombre)
                self.usuarios[value]["nombre"] = value
                self.usuario_actual = value
                self.guardar_datos()

    @property
    def peso(self):
        return self.usuarios[self.usuario_actual]["peso"] if self.usuario_actual else 0.0

    @peso.setter
    def peso(self, value):
        if self.usuario_actual:
            self.usuarios[self.usuario_actual]["peso"] = value
            self.guardar_datos()

    @property
    def estatura(self):
        return self.usuarios[self.usuario_actual]["estatura"] if self.usuario_actual else 0.0

    @estatura.setter
    def estatura(self, value):
        if self.usuario_actual:
            self.usuarios[self.usuario_actual]["estatura"] = value
            self.guardar_datos()

    @property
    def meta_km(self):
        return self.usuarios[self.usuario_actual]["meta_km"] if self.usuario_actual else {}

    @meta_km.setter
    def meta_km(self, value):
        if self.usuario_actual:
            self.usuarios[self.usuario_actual]["meta_km"] = value
            self.guardar_datos()

    @property
    def km_corridos(self):
        return self.usuarios[self.usuario_actual]["km_corridos"] if self.usuario_actual else {}

    @km_corridos.setter
    def km_corridos(self, value):
        if self.usuario_actual:
            self.usuarios[self.usuario_actual]["km_corridos"] = value
            self.guardar_datos()

    @property
    def ejercicios_completados(self):
        return self.usuarios[self.usuario_actual]["ejercicios_completados"] if self.usuario_actual else {}

    @ejercicios_completados.setter
    def ejercicios_completados(self, value):
        if self.usuario_actual:
            self.usuarios[self.usuario_actual]["ejercicios_completados"] = value
            self.guardar_datos()

    @property
    def historial_semanal(self):
        return self.usuarios[self.usuario_actual]["historial_semanal"] if self.usuario_actual else []

    @historial_semanal.setter
    def historial_semanal(self, value):
        if self.usuario_actual:
            self.usuarios[self.usuario_actual]["historial_semanal"] = value
            self.guardar_datos()

    @property
    def mensaje(self):
        return self.usuarios[self.usuario_actual]["mensaje"] if self.usuario_actual else ""

    @mensaje.setter
    def mensaje(self, value):
        if self.usuario_actual:
            self.usuarios[self.usuario_actual]["mensaje"] = value
            self.guardar_datos()

    @property
    def ejercicios_personalizados(self):
        return self.usuarios[self.usuario_actual]["ejercicios_personalizados"] if self.usuario_actual else {}

    @ejercicios_personalizados.setter
    def ejercicios_personalizados(self, value):
        if self.usuario_actual:
            self.usuarios[self.usuario_actual]["ejercicios_personalizados"] = value
            self.guardar_datos()

    def contar_trofeos(self):
        print("Contando trofeos...")
        try:
            return sum(1 for item in self.historial_semanal if item.get("recompensa") == "Crack")
        except Exception as e:
            print(f"Error en contar_trofeos: {e}")
            return 0

    def evaluar_semana(self, get_ejercicios_dia, fecha, get_puntos):
        print(f"Evaluando semana para fecha: {fecha}")
        try:
            semana_ano = fecha.isocalendar()[1]
            ano = fecha.year
            current_week = datetime.now().isocalendar()[1]
            current_year = datetime.now().year
            if ano > current_year or (ano == current_year and semana_ano > current_week):
                return "No se pueden evaluar semanas futuras"

            puntos = 0
            completados_total = 0
            ejercicios_totales = 0
            km_semana = 0.0
            lunes = fecha - timedelta(days=fecha.weekday())

            for i in range(7):
                dia = lunes + timedelta(days=i)
                dia_str = dia.strftime("%Y-%m-%d")
                ejercicios = get_ejercicios_dia(dia) or []
                ejercicios_personalizados = self.ejercicios_personalizados.get(dia_str, [])
                todos_ejercicios = ejercicios + ejercicios_personalizados
                ejercicios_totales += len(todos_ejercicios)
                km_semana += self.km_corridos.get(dia_str, 0.0)
                completados_dia = self.ejercicios_completados.get(dia_str, {})
                for ej in todos_ejercicios:
                    if completados_dia.get(ej, False):
                        completados_total += 1
                        puntos += get_puntos(ej)

            porcentaje_completado = completados_total / ejercicios_totales if ejercicios_totales > 0 else 0

            if puntos >= 300:
                recompensa = "Crack"
                recompensa_texto = "¡Eres una leyenda! 🏆 Elige algo que te haga ilusión para celebrar esta semana épica."
            elif puntos >= 200:
                recompensa = "Chill"
                recompensa_texto = "¡Buen trabajo! 🌟 Disfruta de 30 minutos extra de tiempo de juego esta semana."
            elif puntos >= 100:
                recompensa = "Looser"
                recompensa_texto = "¡Ánimo, puedes mejorar! 😅 Esta semana toca 30 minutos menos de tiempo de juego."
            else:
                recompensa = "Noob"
                recompensa_texto = "¡Venga, a darle caña! 🦴 Ordena tu habitación para empezar con fuerza la próxima semana."

            for item in self.historial_semanal[:]:
                if item["semana"] == semana_ano and item.get("año", ano) == ano:
                    item.update({
                        "puntos": puntos,
                        "completados": porcentaje_completado,
                        "km": km_semana,
                        "recompensa": recompensa,
                        "recompensa_texto": recompensa_texto,
                        "año": ano
                    })
                    break
            else:
                self.historial_semanal.append({
                    "semana": semana_ano,
                    "puntos": puntos,
                    "completados": porcentaje_completado,
                    "km": km_semana,
                    "recompensa": recompensa,
                    "recompensa_texto": recompensa_texto,
                    "año": ano
                })

            self.guardar_datos()
            return puntos, km_semana, completados_total, recompensa, recompensa_texto
        except Exception as e:
            print(f"Error en evaluar_semana: {e}")
            return 0, 0.0, 0, "Noob", "Error al evaluar: ¡Ordena tu habitación y haz 10 flexiones! 😅"