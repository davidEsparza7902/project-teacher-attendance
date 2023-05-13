import tkinter as tk
from ..utils.funciones_sql import *
from ..utils.funciones_analisis import *
from tkinter import ttk
from tkinter import messagebox
import cv2
from ..utils.funciones_sql import *

ruta_img = '.\src\img'
ruta_photo_temp = '.\src\photo_temp'
ruta_photo_analisis = '.\src\photo_analisis'
class form_registro(tk.Toplevel):
    def __init__(self,parent,tipo_fuente,tamano_fuente,peso_fuente):
        super().__init__(parent)
        self.__tipo_fuente = tipo_fuente
        self.__tamano_fuente = tamano_fuente
        self.__peso_fuente = peso_fuente
        self.__administrativo = {
            "dni": "",
            "nombre": "",
            "apellido_paterno": "",
            "apellido_materno": "",
            "area": "",
            "correo": "",
            "contrasenia": ""
        }
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
        self.title('Registro')
        self.geometry('925x500')
        self.centrar()
        self.configure(bg="#fff")
        self.resizable(False,False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        img = tk.PhotoImage(file= ruta_img+"\img-unt.png")
        tk.Label(self,image=img,bg="white").place(x=0,y=0)
        frame = tk.Frame(self,width=350, height=350, bg="white")
        frame.place(x=530,y=70)
        tk.Label(frame,bg='white', text='DNI',font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente)).place(x=20,y=30)
        tk.Label(frame,bg='white', text='Nombre',font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente)).place(x=20,y=60)
        tk.Label(frame,bg='white', text='Apellido Paterno',font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente)).place(x=20,y=90)
        tk.Label(frame,bg='white', text='Apellido Materno',font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente)).place(x=20,y=120)
        tk.Label(frame,bg='white', text='Area',font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente)).place(x=20,y=150)
        tk.Label(frame,bg='white', text='Correo',font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente)).place(x=20,y=180)
        tk.Label(frame,bg='white', text='Contraseña',font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente)).place(x=20,y=210)

        self.__dni = tk.StringVar()
        self.__nombre = tk.StringVar()
        self.__apellido_paterno = tk.StringVar()
        self.__apellido_materno = tk.StringVar()
        self.__correo = tk.StringVar()
        self.__contra = tk.StringVar()
        self.__area = tk.StringVar()
        self.__ruta_foto = ruta_photo_temp

        self.__txt_dni = tk.Entry(frame, textvariable=self.__dni)    
        self.__txt_nombre = tk.Entry(frame, textvariable=self.__nombre)
        self.__txt_apellido_paterno = tk.Entry(frame, textvariable=self.__apellido_paterno)
        self.__txt_apellido_materno = tk.Entry(frame, textvariable=self.__apellido_materno)

        opciones = [
            "Rectorado",
            "Vicerrectorado Académico",
            "Vicerrectorado de Investigación",
            "Vicerrectorado de Extensión",
            "Decanato",
            "Secretaría General",
            "Dirección de Administración y Finanzas",
            "Dirección de Planificación y Evaluación Institucional",
            "Dirección de Recursos Humanos",
            "Dirección de Tecnologías de la Información y Comunicaciones (TIC)",
            "Dirección de Bienestar Universitario",
            "Dirección de Asuntos Estudiantiles",
            "Dirección de Cooperación y Relaciones Internacionales",
            "Dirección de Responsabilidad Social Universitaria",
            "Unidad de Auditoría Interna",
            "Unidad de Control y Gestión de la Calidad",
            "Unidad de Gestión de Proyectos",
            "Unidad de Seguridad y Salud en el Trabajo",
            "Oficina de Relaciones Públicas y Comunicaciones",
            "Oficina de Asesoría Jurídica"
        ]
        self.__cbo_area = ttk.Combobox(frame,values=opciones,state="readonly",textvariable=self.__area)

        self.__txt_correo = tk.Entry(frame, textvariable=self.__correo)
        self.__txt_contra = tk.Entry(frame, textvariable=self.__contra,show='*')
    
        self.__txt_dni.place(x=200,y=30)
        self.__txt_nombre.place(x=200,y=60)
        self.__txt_apellido_paterno.place(x=200,y=90)
        self.__txt_apellido_materno.place(x=200,y=120)
        self.__cbo_area.place(x=200,y=150)
        self.__txt_correo.place(x=200,y=180)
        self.__txt_contra.place(x=200,y=210)
        
        
        btn_registrar=tk.Button(frame,command=self.validar_registrar, pady=7,font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente), text="REGISTRAR",fg="white", bg="green",relief='groove')
        btn_registrar.place(x=50,y=250)
        btn_registrar.configure(padx=20)
        btn_cancelar=tk.Button(frame,command=self.on_closing, pady=7,font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente), text="CANCELAR",fg="white", bg="red",relief='groove')
        btn_cancelar.place(x=200,y=250)
        self.__txt_dni.focus()
        self.mainloop()
    def limpiar_entradas(self):
        self.__txt_dni.delete(0,tk.END)
        self.__txt_nombre.delete(0,tk.END)
        self.__txt_apellido_paterno.delete(0,tk.END)
        self.__txt_apellido_materno.delete(0,tk.END)
        self.__txt_correo.delete(0,tk.END)
        self.__txt_contra.delete(0,tk.END)
        # Seleccionar el primer elemento del combobox
        self.__cbo_area.current(0)
        self.__txt_dni.focus()
    def limpiar_variables(self):
        self.__dni.set("")
        self.__nombre.set("")
        self.__apellido_paterno.set("")
        self.__apellido_materno.set("")
        self.__area.set("")
        self.__correo.set("")
        self.__contra.set("")
        self.__ruta_foto = ""
        
    def registro_facial (self):
        # Captura de imagen
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret == False: break
            cv2.imshow('Registro Facial',frame)
            k = cv2.waitKey(1)
            if k == 27:
                break
        dni_img = self.__dni.get()
        ruta_img_temp = ruta_photo_temp+"\\"+dni_img+".jpg"
        cv2.imwrite(ruta_img_temp,frame)
        cap.release()
        cv2.destroyAllWindows()

        
        generar_analisis_imagen_registrada(ruta_img_temp)
        self.setAdministrativo()
        # Insertar administrativo
        insertar_administrativo(self.__administrativo)
        messagebox.showinfo(message="Registro facial exitoso", title="Registro facial")
        
        
    def setAdministrativo(self):
        self.__administrativo = {
            "dni": self.__dni.get(),
            "nombre": self.__nombre.get(),
            "apellido_paterno": self.__apellido_paterno.get(),
            "apellido_materno": self.__apellido_materno.get(),
            "area": self.__area.get(),
            "correo": self.__correo.get(),
            "contrasenia": self.__contra.get()
        }
    def registrar_usuario(self):
        self.registro_facial()
        self.limpiar_variables()
        # Mostrar mensaje de exito
        tk.messagebox.showinfo(title="Registro", message="Administrativo registrado correctamente")
        self.on_closing()
    def es_valido(self):
        valido = True
        # Validar entradas
        # imprimir las variables
        if self.__dni.get() != "" and self.__nombre.get() != "" and self.__apellido_paterno.get() != "" and self.__apellido_materno.get() != "" and self.__area.get() != "" and self.__correo.get() != "" and self.__contra.get() != "":
            if len(self.__dni.get()) != 8 or len(self.__contra.get()) < 8:
                valido = False
                print("El dni debe tener 8 digitos y la contraseña debe tener al menos 8 caracteres")
        else:
            valido = False
            print("Todos los campos son obligatorios")

        if valido: # Validar que el dni no se repita en la base de datos
            if buscarDNI(self.__dni.get()) != None:
                valido = False
                print("El dni ya existe")
        return valido
    
    def validar_registrar(self):
        if self.es_valido():
            self.registrar_usuario()
        else:
            tk.messagebox.showerror(title="Registro", message="No se pudo registrar el Administrativo")

        