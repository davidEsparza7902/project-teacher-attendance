from src.presentation.form_principal import form_principal

ruta_img = ".\src\img"
tipo_fuente = "Segoe UI"
tamano_fuente = 12
peso_fuente = "bold"

def cargar_ventana_principal():
    frm_principal = form_principal(tipo_fuente, tamano_fuente, peso_fuente)
    frm_principal.mostrar()
if __name__ == "__main__":
    cargar_ventana_principal()