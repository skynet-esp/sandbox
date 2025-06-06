import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk

from datetime import datetime, timedelta



def get_week_dates(week_number, year):

    """Devuelve las fechas de lunes y domingo para una semana dada en formato dd/mm."""

    try:

        first_day = datetime.strptime(f"{year}-W{week_number-1}-1", "%Y-W%W-%w").date()

        last_day = first_day + timedelta(days=6)

        return first_day.strftime("%d/%m"), last_day.strftime("%d/%m")

    except Exception as e:

        print(f"Error en get_week_dates: {e}")

        return "N/A", "N/A"



def mostrar_informe_progreso(modelo):

    root = tk.Tk()

    root.title("Gráficos de Progreso Semanal")

    root.geometry("800x600")

    root.configure(bg="#ffffff")



    if not modelo.historial_semanal:

        tk.Label(root, text="No hay datos de semanas evaluadas.", font=("Arial", 12), bg="#ffffff").pack(pady=20)

        root.mainloop()

        return



    try:

        current_week = datetime.now().isocalendar()[1]

        current_year = datetime.now().year

        historial_filtrado = [

            item for item in modelo.historial_semanal

            if item.get("año", current_year) <= current_year and item["semana"] <= current_week

        ]

        historial_ordenado = sorted(historial_filtrado, key=lambda x: (x.get("año", current_year), x["semana"]))

        semanas = [item["semana"] for item in historial_ordenado]

        puntos = [item["puntos"] for item in historial_ordenado]

        completados = [item["completados"] * 100 for item in historial_ordenado]

        fechas = [f"{get_week_dates(semana, item.get('año', current_year))[0]} al {get_week_dates(semana, item.get('año', current_year))[1]}" 

                  for item in historial_ordenado]



        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7))



        ax1.bar(range(len(semanas)), puntos, color="#ff69b4", edgecolor="black", alpha=0.8)

        ax1.set_title("Puntos por Semana", fontsize=12, fontweight="bold")

        ax1.set_xlabel("Semana", fontsize=10)

        ax1.set_ylabel("Puntos", fontsize=10)

        ax1.set_xticks(range(len(semanas)))

        ax1.set_xticklabels(fechas, rotation=45, ha="right", fontsize=8)

        ax1.grid(True, axis="y", linestyle="--", alpha=0.7, color="#d3d3d3")

        for i, v in enumerate(puntos):

            ax1.text(i, v + 0.5, str(v), ha="center", fontsize=9, color="#ff69b4")



        ax2.plot(range(len(semanas)), completados, color="#00ced1", marker="o", linewidth=2, markersize=7)

        ax2.set_title("% Ejercicios Completados", fontsize=12, fontweight="bold")

        ax2.set_xlabel("Semana", fontsize=10)

        ax2.set_ylabel("Porcentaje (%)", fontsize=10)

        ax2.set_xticks(range(len(semanas)))

        ax2.set_xticklabels(fechas, rotation=45, ha="right", fontsize=8)

        ax2.grid(True, axis="y", linestyle="--", alpha=0.7, color="#d3d3d3")

        for i, v in enumerate(completados):

            ax2.text(i, v + 2, f"{v:.1f}%", ha="center", fontsize=9, color="#00ced1")



        plt.tight_layout()



        canvas = FigureCanvasTkAgg(fig, master=root)

        canvas.draw()

        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        tk.Button(root, text="Cerrar", font=("Arial", 10), bg="#f3f4f6", fg="black", command=root.destroy, relief="flat").pack(pady=10)

        plt.close(fig)

        root.mainloop()

    except Exception as e:

        print(f"Error en mostrar_informe_progreso: {e}")

        tk.Label(root, text="Error al generar gráficos.", font=("Arial", 12), bg="#ffffff").pack(pady=20)

        root.mainloop()