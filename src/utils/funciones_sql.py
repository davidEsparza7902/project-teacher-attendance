import numpy as np
import os
import cv2
from datetime import datetime
import mysql.connector
from mysql.connector import Error
ruta_photo_temp = '.\src\photo_temp'
ruta_photo_analisis = '.\src\photo_analisis'


def conectar():
    try: 
        conexion = mysql.connector.connect(host='localhost',
                                    port=3306,
                                    user='root',
                                    password='root',
                                    db='bd_asistencia_administrativa_unt')
    except Error as ex:
        pass
    return conexion

def reporte_nro_asistencias(dni):

    db = conectar()
    cursor = db.cursor()
    query = '''SELECT TIPO_ASISTENCIA, COUNT(*) FROM ASISTENCIA WHERE DNI_ADMINISTRATIVO LIKE %s GROUP BY TIPO_ASISTENCIA'''
    values = (dni,)
    cursor.execute(query,values)
    datos = []
    for fila in cursor.fetchall():
        datos.append(fila)
    arreglo = np.array(datos)
    cursor.close()
    db.close()
    return arreglo

def get_administrativo(dni):
    db = conectar()
    cursor = db.cursor()
    query = '''SELECT * FROM ADMINISTRATIVO WHERE DNI LIKE %s'''
    valores = (dni,)
    cursor.execute(query,valores)
    resultado = cursor.fetchone()
    ruta_imagen = ruta_photo_temp+"\\"+resultado[0]+".jpg"
    if os.path.exists(ruta_imagen):
        os.remove(ruta_imagen)
    imagen_bytes = resultado[7]
    np_array = np.frombuffer(imagen_bytes, np.uint8)
    imagen = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    cv2.imwrite(ruta_imagen, imagen)
    administrativo = { "dni": resultado[0], 
                  "nombre": resultado[1], 
                  "apellido_paterno": resultado[2],
                   "apellido_materno": resultado[3],
                   "area": resultado[4],
                   "contrasenia": resultado[5],
                    "correo": resultado[6],
                    "ruta_foto": ruta_imagen
                    }
    cursor.close()
    db.close()
    return administrativo
def buscarDNI(dni):
    db = conectar()
    cursor = db.cursor()
    cursor.execute("SELECT dni FROM Administrativo WHERE dni = %s", (dni,))
    resultado = cursor.fetchone()
    cursor.close()
    db.close()
    return resultado
def administrativo_valido(correo, contrasenia):
    db = conectar()
    cursor = db.cursor()
    query = '''SELECT dni FROM Administrativo 
                WHERE correo = %s AND contrasenia = %s'''
    valores = (correo,contrasenia,)
    cursor.execute(query, valores)
    resultado = cursor.fetchone()
    cursor.close()
    db.close()
    return resultado != None
def insertar_administrativo(administrativo):
    ruta = ruta_photo_temp+"\\"+administrativo["dni"]+".jpg"
    print("\nRuta de guardado: ",ruta)
    foto = cv2.imread(ruta)
    encoded_foto = cv2.imencode(".jpg", foto)[1].tobytes()
    db = conectar()
    cursor = db.cursor()
    query = '''INSERT INTO Administrativo (dni, nombre, apellido_paterno,apellido_materno,
                area,contrasenia,correo,foto) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    values = (administrativo["dni"],
              administrativo["nombre"],
              administrativo["apellido_paterno"],
              administrativo["apellido_materno"],
              administrativo["area"],
              administrativo["contrasenia"],
              administrativo["correo"],
              encoded_foto,)
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()
def get_administrativo(correo,contrasenia):
    db = conectar()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Administrativo WHERE correo = %s AND contrasenia = %s", (correo,contrasenia,))
    resultado = cursor.fetchone()
    ruta_imagen = ".\src\photo_temp\\"+resultado[0]+".jpg"
    if os.path.exists(ruta_imagen):
        os.remove(ruta_imagen)

    imagen_bytes = resultado[7]
    np_array = np.frombuffer(imagen_bytes, np.uint8)
    imagen = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
    cv2.imwrite(ruta_imagen, imagen)
    administrativo = { "dni": resultado[0], 
                  "nombre": resultado[1], 
                  "apellido_paterno": resultado[2],
                   "apellido_materno": resultado[3],
                   "area": resultado[4],
                   "contrasenia": resultado[5],
                    "correo": resultado[6],
                    "ruta_foto": ruta_imagen
                    }
    cursor.close()
    db.close()
    return administrativo
def registrar_asistencia(dni_administrativo):
    dia = datetime.today().strftime('%Y-%m-%d')
    hora = datetime.now().time()
    query = ''' SELECT * FROM ASISTENCIA WHERE DNI_ADMINISTRATIVO LIKE %s AND FECHA = %s'''
    values = (dni_administrativo,dia,)
    db = conectar()
    cursor = db.cursor()
    cursor.execute(query,values)
    resultados = cursor.fetchall()
    if not resultados:
        if hora < datetime.strptime('13:00:00', '%H:%M:%S').time():
            if hora > datetime.strptime('08:00:00', '%H:%M:%S').time():
                # Registrar tardanza
                print("Tardanza")
                query = '''INSERT INTO ASISTENCIA (DNI_ADMINISTRATIVO, FECHA, HORA_ENTRADA, TIPO_ASISTENCIA) 
                           VALUES (%s,%s,%s,"TARDANZA")'''
            else: 
                # Registrar asistencia
                if hora > datetime.strptime('05:00:00', '%H:%M:%S').time():
                    print("Presente")
                    query = '''INSERT INTO ASISTENCIA (DNI_ADMINISTRATIVO, FECHA, HORA_ENTRADA, TIPO_ASISTENCIA) 
                               VALUES (%s,%s,%s,"PRESENTE")'''
            values = (dni_administrativo, dia, hora,)
            cursor.execute(query, values)
        else:
            # Registrar falta
            print("Falta")
            values = (dni_administrativo, dia,)
            query = '''INSERT INTO ASISTENCIA (DNI_ADMINISTRATIVO, FECHA, TIPO_ASISTENCIA) VALUES (%s,%s,"FALTA")'''
            cursor.execute(query, values)

    else:
        hora_entrada = resultados[0][3]
        if hora_entrada:
            # Registrar hora de salida
            print("Registrando hora de salida")
            query = '''UPDATE ASISTENCIA SET HORA_SALIDA=%s WHERE DNI_ADMINISTRATIVO = %s AND FECHA = %s'''
            values = (hora, dni_administrativo, dia)
            cursor.execute(query, values)
    db.commit()

    cursor.close()
    db.close()

