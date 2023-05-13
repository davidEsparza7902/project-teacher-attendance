import tkinter as tk
from .form_usuario import form_usuario
from ..utils.funciones_sql import *
ruta_img = ".\src\img"
ruta_photo_temp = '.\src\photo_temp'
ruta_photo_analisis = '.\src\photo_analisis'
class form_login (tk.Toplevel):
    def __init__(self, parent, tipo_fuente, tamano_fuente, peso_fuente):
        super().__init__(parent)
        self.__tipo_fuente = tipo_fuente
        self.__tamano_fuente = tamano_fuente
        self.__peso_fuente = peso_fuente

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
        self.title('Login')
        self.geometry('925x500')
        self.centrar()
        self.configure(bg="#fff")
        self.resizable(False,False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        img = tk.PhotoImage(file= ruta_img+"\img-unt.png")
        logo = tk.Label(self,image=img,bg="white")
        frame = tk.Frame(self,width=350, height=350, bg="white")
        lbl_titulo = tk.Label(frame,bg='white', text='Iniciar Sesión',font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente))
        lbl_correo = tk.Label(frame,bg='white', text='Correo',font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente))
        lbl_contra = tk.Label(frame,bg='white', text='Contraseña',font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente))
        self.__correo = tk.StringVar()
        self.__contrasenia = tk.StringVar()
        txt_correo = tk.Entry(frame ,width=30, textvariable=self.__correo,font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente))        
        txt_contra = tk.Entry(frame ,width=30, textvariable=self.__contrasenia,font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente),show="*")

        btn_login = tk.Button(frame, text='Ingresar',bg="blue",fg="white",font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente),command=self.validar_login)
        btn_cancelar = tk.Button(frame, text='Cancelar',bg="red",fg="white",font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente),command=self.on_closing)
        
        logo.place(x=0,y=0)
        frame.place(x=530,y=70)
        lbl_titulo.place(x=100,y=0)
        lbl_correo.place(x=20,y=30)
        lbl_contra.place(x=20,y=60)
        txt_correo.place(x=120,y=30)
        txt_contra.place(x=120,y=60)
        btn_login.place(x=80,y=100)
        btn_cancelar.place(x=200,y=100)
        self.mainloop()
    def es_valido(self):
        valido = True
        correo = self.__correo.get()
        contrasenia = self.__contrasenia.get()
        
        if correo !="" and contrasenia !="" and len(contrasenia) >= 8:
            if not administrativo_valido(correo, contrasenia):
                valido = False
        else:
            valido = False
        return valido

    def validar_login(self):
        if self.es_valido():
            self.login()
        else:
            tk.messagebox.showerror(title="Registro", message="Datos no válidos")
    def login(self):
        # verificar que los datos ingresados estén en la base de datos
        administrativo = get_administrativo(self.__correo.get(), self.__contrasenia.get())
        frm_usuario = form_usuario(self,administrativo, self.__tipo_fuente, self.__tamano_fuente, self.__peso_fuente)
        frm_usuario.mostrar()
        