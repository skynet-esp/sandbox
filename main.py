import tkinter as tk



from tkinter import messagebox



from modelo import Modelo



from ejercicios import Ejercicios



from interfaz import Interfaz







if __name__ == "__main__":



    try:



        root = tk.Tk()



        modelo = Modelo()



        ejercicios = Ejercicios()



        app = Interfaz(root, modelo, ejercicios)



        root.mainloop()



    except Exception as e:



        root = tk.Tk()



        root.withdraw()  # Oculta la ventana principal



        messagebox.showerror("Error", f"La aplicación falló al iniciarse: {str(e)}")



        root.destroy()