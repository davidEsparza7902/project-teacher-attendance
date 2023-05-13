import cv2
from matplotlib import pyplot
from mtcnn import MTCNN
ruta_photo_temp = '.\src\photo_temp'
ruta_photo_analisis = '.\src\photo_analisis'
def generar_analisis_imagen_registrada(ruta_img):
    pixeles = pyplot.imread(ruta_img)
    detector = MTCNN()
    lista_resultados = detector.detect_faces(pixeles)
    if len(lista_resultados)>=1:
        guardar_analisis_imagen_registrada(ruta_img,lista_resultados)
def guardar_analisis_imagen_registrada (ruta_img,lista_resultados):
    dni = ruta_img.split("\\")[-1].split(".")[0]
    data = pyplot.imread(ruta_img)
    for i in range(len(lista_resultados)):
        x1,y1,ancho, alto = lista_resultados[i]['box']
        x2,y2 = x1 + ancho, y1 + alto
        pyplot.subplot(1, len(lista_resultados), i+1)
        pyplot.axis('off')
        cara_reg = data[y1:y2, x1:x2]
        cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen con un tamaño de 150x200
        ruta = ruta_photo_analisis+"\\"+dni+".jpg"
        cv2.imwrite(ruta,cara_reg)
def generar_analisis_imagen_login(ruta_img):
    pixeles = pyplot.imread(ruta_img)
    detector = MTCNN()
    resultados = detector.detect_faces(pixeles)
    if len(resultados)>=1:
        guardar_analisis_imagen_login(ruta_img,resultados)
def guardar_analisis_imagen_login(ruta_img,lista_resultados):
    dni = ruta_img.split("\\")[-1].split("_login.")[0]
    data = pyplot.imread(ruta_img)
    for i in range(len(lista_resultados)):
        x1,y1,ancho, alto = lista_resultados[i]['box']
        x2,y2 = x1 + ancho, y1 + alto
        pyplot.subplot(1, len(lista_resultados), i+1)
        pyplot.axis('off')
        cara_reg = data[y1:y2, x1:x2]
        cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen 150x200
        ruta = ruta_photo_analisis+"\\"+dni+"_login.jpg"
        cv2.imwrite(ruta,cara_reg)
        #return pyplot.imshow(data[y1:y2, x1:x2])
    #pyplot.show()
def orb_sim(img1,img2):
    orb = cv2.ORB_create()  #Creamos el objeto de comparacion
    kpa, descr_a = orb.detectAndCompute(img1, None)  #Creamos descriptor 1 y extraemos puntos claves
    kpb, descr_b = orb.detectAndCompute(img2, None)  #Creamos descriptor 2 y extraemos puntos claves
    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) #Creamos comparador de fuerza
    matches = comp.match(descr_a, descr_b)  #Aplicamos el comparador a los descriptores
    regiones_similares = [i for i in matches if i.distance < 70] #Extraemos las regiones similares en base a los puntos claves
    if len(matches) == 0:
        return 0
    return len(regiones_similares)/len(matches)  #Exportamos el porcentaje de similitud
        
