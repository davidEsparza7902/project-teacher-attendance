from .form_registro import form_registro
from .form_login import form_login
import tkinter as tk
from tkinter import messagebox
ruta_img = '.\src\img'
class form_principal(tk.Tk):
    def __init__(self,tipo_fuente,tamano_fuente,peso_fuente):
        super().__init__()
        self.__tipo_fuente = tipo_fuente
        self.__tamano_fuente = tamano_fuente
        self.__peso_fuente = peso_fuente
    def on_closing(self):
        if  messagebox.askokcancel("Salir", "¿Desea salir?"):
            self.destroy()
            self.quit()
    def centrar(self):
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x_ventana = self.winfo_screenwidth() // 2 - ancho // 2
        y_ventana = self.winfo_screenheight() // 2 - alto // 2
        self.geometry("+{}+{}".format(x_ventana, y_ventana))
    def mostrar(self):
        self.title("Sistema de Control Asistencia UNT")
        self.geometry("410x460")
        self.centrar()
        self.configure(bg="#fff")
        self.resizable(False,False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        ph = tk.PhotoImage(file = ruta_img+"\logo.png")
        phimg = ph.subsample(6, 6)
        photo = tk.PhotoImage(file = ruta_img+"\login.png")
        photoimage = photo.subsample(6, 6)
        photo2 = tk.PhotoImage(file = ruta_img+"\img-registro.png")
        photoimage2 = photo2.subsample(6, 6)

        lbl_logo = tk.Label(bg="white",image=phimg,width = "410",height = "150")
        lbl_logo.pack(side = tk.TOP,pady=20)
        lbl_titulo = tk.Label(text="SISTEMA DE ASISTENCIA\n UNIVERSIDAD NACIONAL DE TRUJILLO",bg="white",font=(self.__tipo_fuente,self.__tamano_fuente,self.__peso_fuente))
        lbl_titulo.pack(side = tk.TOP, pady=10)
        btn_login = tk.Button(text = "Log In", command=self.ventana_login, font=(self.__tipo_fuente,self.__tamano_fuente),relief="groove",height = "40", width = "120",image=photoimage,compound=tk.LEFT,bg="blue",fg="white")
        btn_login.pack(side = tk.TOP)
        btn_registrar = tk.Button(text = "Registrarse", command = self.abrir_ventana_registro, font=(self.__tipo_fuente,self.__tamano_fuente),relief="groove",height = "40", width = "120",image=photoimage2,compound= tk.LEFT,bg="green",fg="white")
        btn_registrar.pack(side = tk.TOP,pady=20)
        self.mainloop()
        
    def ventana_login(self):
        frm_login = form_login(self, self.__tipo_fuente, self.__tamano_fuente, self.__peso_fuente)
        frm_login.grab_set()   # Establecer el foco en el formulario secundario 
        frm_login.transient(self) # Establecer el formulario secundario como dependiente del formulario principal
        frm_login.mostrar() # Mostrar el formulario secundario
        if frm_login.winfo_exists():
            frm_login.wait_visibility() # Esperar hasta que el formulario secundario sea visible
            frm_login.wait_window() # Esperar hasta que se cierre el formulario secundario
            frm_login.grab_release()  # Liberar el foco del formulario secundario
    def abrir_ventana_registro(self):
        frm_registro = form_registro(self, self.__tipo_fuente, self.__tamano_fuente, self.__peso_fuente)
        frm_registro.grab_set()   # Establecer el foco en el formulario secundario 
        frm_registro.transient(self) # Establecer el formulario secundario como dependiente del formulario principal
        frm_registro.mostrar() # Mostrar el formulario secundario
        if frm_registro.winfo_exists():
            frm_registro.wait_visibility() # Esperar hasta que el formulario secundario sea visible
            frm_registro.wait_window() # Esperar hasta que se cierre el formulario secundario
            frm_registro.grab_release()  # Liberar el foco del formulario secundario
        
