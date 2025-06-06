from datetime import datetime
import random

class Ejercicios:
    def __init__(self):
        # Lista ampliada de ejercicios para hiperlordosis
        self.hiperlordosis_ejercicios = [
            ("Puente de glúteos bilateral", "fortalecimiento"),
            ("Puente de glúteos unilateral", "fortalecimiento"),
            ("Plancha isométrica baja", "fortalecimiento"),
            ("Elevación pélvica con apoyo", "fortalecimiento"),
            ("Gato-vaca", "movilidad"),
            ("Estiramiento de psoas en zancada", "estiramiento"),
            ("Estiramiento de isquiotibiales supino", "estiramiento"),
            ("Rotación espinal suave", "movilidad"),
            ("Abdominales de contracción isométrica", "fortalecimiento")
        ]
        # Base exercises for a 13-year-old, 4 general + 2 for hyperlordosis
        self.base_ejercicios = [
            # Lunes
            [
                "Flexiones de rodillas",
                "Sentadillas con apoyo",
                "Abdominales crunch suaves",
                "Zancadas cortas"
            ],
            # Martes
            [
                "Burpees modificados",
                "Elevaciones de talones",
                "Plancha frontal corta",
                "Saltos suaves"
            ],
            # Miércoles
            [
                "Escaladores lentos",
                "Fondos en silla",
                "Subidas al step bajas",
                "Abdominales bicicleta suaves"
            ],
            # Jueves
            [
                "Flexiones inclinadas (en mesa)",
                "Sentadillas libres",
                "Plancha lateral corta",
                "Zancadas laterales cortas"
            ],
            # Viernes
            [
                "Burpees modificados",
                "Saltos verticales suaves",
                "Abdominales en V suaves",
                "Elevaciones de pelvis"
            ],
            # Sábado
            [
                "Saltos patinador lentos",
                "Flexiones de rodillas",
                "Abdominales crunch suaves",
                "Movilidad de cadera"
            ],
            # Domingo (recovery-focused)
            [
                "Estiramientos dinámicos",
                "Movilidad articular suave",
                "Respiración diafragmática",
                "Yoga suave (posturas básicas)"
            ]
        ]

    def get_ejercicios_dia(self, fecha):
        try:
            dia_semana = fecha.weekday()
            semana_ano = fecha.isocalendar()[1]
            ejercicios_generales = self.base_ejercicios[dia_semana]
            ciclo = (semana_ano - 1) % 16  # 16-week progression cycle
            # Progressive overload for general exercises
            if ciclo < 4:  # Weeks 1-4
                series = 2
                repeticiones = 8
            elif ciclo < 8:  # Weeks 5-8
                series = 2
                repeticiones = 10
            elif ciclo < 12:  # Weeks 9-12
                series = 3
                repeticiones = 10
            else:  # Weeks 13-16
                series = 3
                repeticiones = 12

            # Progressive overload for hyperlordosis exercises
            if ciclo < 4:
                series_hiper = 2
                repeticiones_hiper = 12
                segundos_hiper = 45
            elif ciclo < 8:
                series_hiper = 2
                repeticiones_hiper = 15
                segundos_hiper = 60
            elif ciclo < 12:
                series_hiper = 3
                repeticiones_hiper = 15
                segundos_hiper = 60
            else:
                series_hiper = 3
                repeticiones_hiper = 18
                segundos_hiper = 75

            # Seleccionar 2 ejercicios para hiperlordosis (1 fortalecimiento, 1 estiramiento/movilidad)
            fortalecimiento = random.choice([e for e, t in self.hiperlordosis_ejercicios if t == "fortalecimiento"])
            movilidad_estiramiento = random.choice([e for e, t in self.hiperlordosis_ejercicios if t in ["movilidad", "estiramiento"]])

            ejercicios_progresivos = []
            # General exercises
            for ej in ejercicios_generales:
                ejercicios_progresivos.append(f"{series} series de {repeticiones} {ej}")
            # Hiperlordosis exercises
            ejercicios_progresivos.append(f"{series_hiper} series de {repeticiones_hiper} {fortalecimiento}")
            ejercicios_progresivos.append(f"{series_hiper} series de {segundos_hiper} segundos {movilidad_estiramiento}")
            return ejercicios_progresivos[:6]
        except Exception as e:
            print(f"Error en get_ejercicios_dia: {e}")
            return ["Ejercicio no disponible"] * 6

    def get_puntos(self, ejercicio):
        """
        Devuelve los puntos asociados con un ejercicio dado.
        Ejercicios generales: 5 puntos
        Ejercicios de hiperlordosis: 10 puntos
        """
        try:
            # Verifica si el ejercicio es de hiperlordosis
            for ej, tipo in self.hiperlordosis_ejercicios:
                if ej in ejercicio:  # Comprueba si el nombre base del ejercicio está en la cadena
                    return 10  # Más puntos para ejercicios de hiperlordosis
            return 5  # Puntos por defecto para ejercicios generales y personalizados
        except Exception as e:
            print(f"Error en get_puntos: {e}")
            return 0  # Devuelve 0 puntos en caso de error