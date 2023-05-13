import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ..utils.funciones_sql import reporte_nro_asistencias
import tkinter as tk
from tkinter import ttk
ruta_img = '.\src\img'
ruta_photo_temp = '.\src\photo_temp'
ruta_photo_analisis = '.\src\photo_analisis'
class form_reporte(tk.Toplevel):
    def __init__(self,parent,dni):
        super().__init__(parent)
        self.__dni = dni
    def centrar(self):
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x_ventana = self.winfo_screenwidth() // 2 - ancho // 2
        y_ventana = self.winfo_screenheight() // 2 - alto // 2
        self.geometry("+{}+{}".format(x_ventana, y_ventana))
    def on_closing(self):
        self.destroy()
        self.quit()
    def mostrar(self):
        self.title('Reporte')
        self.geometry('1000x800')
        self.centrar()
        self.configure(bg="#fff")
        self.resizable(False,False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.graficar()
        self.mainloop()
    def tabla_nro_asistencias(self):
        arreglo = reporte_nro_asistencias(self.__dni)
        tabla = tk.Frame(self)
        tabla.place(x=500,y=10)
        tipo_asistencia = tk.Label(tabla, text='Tipo Asistencia', bg='#fff', fg='#000', font=('Arial', 12))
        tipo_asistencia.grid(row=0, column=0, padx=10, pady=10)
        nro_asistencias = tk.Label(tabla, text='Nro Asistencias', bg='#fff', fg='#000', font=('Arial', 12))
        nro_asistencias.grid(row=0, column=1, padx=10, pady=10)
        for i,(pais, nro) in enumerate(arreglo):
            pais = tk.Label(tabla, text=pais, bg='#fff', fg='#000', font=('Arial', 12))
            pais.grid(row=i+1, column=0, padx=10, pady=10)
            nro = tk.Label(tabla, text=nro, bg='#fff', fg='#000', font=('Arial', 12))
            nro.grid(row=i+1, column=1, padx=10, pady=10)
        
    def grafico_circular_nro_asistencias(self):
        arreglo = reporte_nro_asistencias(self.__dni)
        fig, ax = plt.subplots()
        ax.pie(arreglo[:, 1], labels=arreglo[:, 0], autopct='%1.1f%%')
        ax.set_title('Distribución de Asistencias')
        fig.set_size_inches(4, 4)
        canvas = FigureCanvasTkAgg(fig, master = self)
        canvas.draw()
        canvas.get_tk_widget().place(x=40, y = 10)
    def graficar(self):
        self.grafico_circular_nro_asistencias()
        self.tabla_nro_asistencias()
