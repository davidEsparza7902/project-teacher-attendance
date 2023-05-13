from  .form_reporte import form_reporte
from ..utils.funciones_analisis import *
from ..utils.funciones_sql import *
import tkinter as tk
from tkinter import messagebox
import cv2

ruta_img = ".\src\img"
ruta_photo_temp = '.\src\photo_temp'
ruta_photo_analisis = '.\src\photo_analisis'
class form_usuario(tk.Toplevel):
    def __init__(self,parent,administrativo,tipo_fuente,tamano_fuente,peso_fuente):
        super().__init__(parent)
        self.__tipo_fuente = tipo_fuente
        self.__tamano_fuente = tamano_fuente
        self.__peso_fuente = peso_fuente 
        self.__administrativo = administrativo
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
        self.title('Administrativo')
        self.geometry('525x500')
        self.centrar()
        self.configure(bg="#fff")
        self.resizable(False,False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        ph = tk.PhotoImage(file = ruta_img+"\logo.png")
        logo = ph.subsample(6, 6)
        banner = tk.Label(self,image=logo,bg="white",width = "410",height = "150")
        banner.pack(side = tk.TOP,pady=20)
        lbl_bienvenido = tk.Label(self,text="Bienvenido "+ self.__administrativo["nombre"].capitalize()+" "+self.__administrativo["apellido_paterno"].capitalize()+" "+ self.__administrativo["apellido_materno"].capitalize() ,bg="white",fg="blue",font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente))
        lbl_bienvenido.pack(side = tk.TOP, pady=10)
        lbl_dni = tk.Label(self,text="DNI: "+self.__administrativo["dni"],bg="white",fg="black",font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente))
        lbl_dni.pack(side = tk.TOP, pady=5)
        lbl_area = tk.Label(self,text="Area: "+self.__administrativo["area"],bg="white",fg="black",font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente))
        lbl_area.pack(side = tk.TOP, pady=5)
        lbl_correo = tk.Label(self,text="Correo: "+self.__administrativo["correo"],bg="white",fg="black",font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente))
        lbl_correo.pack(side = tk.TOP, pady=5)
        btn_registrar_asistencia = tk.Button(self,command=self.accion_asistencia,text="Registrar Asistencia",bg="blue",fg="white",font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente))
        btn_reporte_asistencia = tk.Button(self,command = self.ventana_reporte,text="Reporte Asistencia",bg="green",fg="white",font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente))
        btn_cerrar_sesion = tk.Button(self,command=self.on_closing,text="Cerrar Sesion",bg="red",fg="white",font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente))
        btn_registrar_asistencia.pack(side = tk.TOP, pady=5)
        btn_reporte_asistencia.pack(side = tk.TOP, pady=5)
        btn_cerrar_sesion.pack(side = tk.TOP, pady=5)
        
        self.mainloop()
    def ventana_reporte(self):
        frm_reporte = form_reporte (self,self.__administrativo["dni"])
        frm_reporte.mostrar()
    def accion_asistencia(self):
        captura = cv2.VideoCapture(0)
        while True:
            ret, frame = captura.read()
            cv2.imshow('Camara',frame)
            if cv2.waitKey(1) == 27:
                break
        ruta_foto_login = ruta_photo_temp+"\\"+self.__administrativo["dni"]+"_login.jpg"
        cv2.imwrite(ruta_foto_login,frame)
        captura.release()
        cv2.destroyAllWindows()

        generar_analisis_imagen_login(ruta_foto_login)
        ruta_imagen_almacenada_analisis = ruta_photo_analisis+"\\"+self.__administrativo["dni"]+".jpg"
        ruta_imagen_login_analisis = ruta_photo_analisis+"\\"+self.__administrativo["dni"]+"_login.jpg"
        imagen_almacenada_analisis = cv2.imread(ruta_imagen_almacenada_analisis)
        imagen_login_analisis = cv2.imread(ruta_imagen_login_analisis)
        similitud = orb_sim(imagen_almacenada_analisis,imagen_login_analisis)
        if similitud >= 0.7:
            registrar_asistencia(self.__administrativo["dni"])
            messagebox.showinfo("Registrar asistencia","Asistencia registrada.") # título, mensaje
            print("Compatibilidad con la foto del registro al: ",similitud)
        else:
            print("Rostro incorrecto, Verifique Identidad")
            print("Compatibilidad con la foto del registro: ",similitud)
            messagebox.showinfo("Error", "No se encuentran coincidencias. Reintentar") # título, mensaje
        
          
        


    

        