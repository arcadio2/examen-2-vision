from ArcadioCv import * 
from Kmeans import * 
from Kmeans2D import * 
from Analisis2D import * 
import cv2


"""
    Esta función crea k imagenes, dependiendo de los centroides dados en el Kmeans que segmenta por
    colores, de manera que aplica el log a cada imagen, de esta manera obtenemos los objetos
    separados por color, y así podemos obtener los jitomates que serían un rojo
"""
def crear_imagenes(coordenadas,imagen):
    rows,cols,colors = imagen.shape
    imagenes = []
    for k in coordenadas:
        imagen = np.zeros((rows,cols),np.uint8)
        indices = k.get('indices')
        for indice in indices:
            i = indice[0]
            j = indice[1]
            if(indice == (i,j)):
                #print("xdxd")
                #guardamos el valor
                imagen[i,j] = 255
        imagenes.append(imagen)

    imagenes_log = []
    index = 0
    for imagen in imagenes:
        #grises = ArcadioCv.rgb_to_grises(imagen)
        cv2.imwrite(f'images/Jit_k_{str(index)}.png',imagen)
        imagen_cruces, imagen_delta,imagen_final,imagen_log = ArcadioCv.filtro_log(imagen,7,1)
        ArcadioCv.visualizar_imagen(imagen_final)
        imagenes_log.append(imagen_final)
        index+=1
    return imagenes_log


"""
    Esta función ya no se usa, pero nos rellenaba completamente los jitomates
"""
def fill():
     #invertir colores
    imagen = ArcadioCv.abrir_imagen_grises("images/Jit_k_2.png")
    rows,cols =imagen.shape
    print(imagen)
    ArcadioCv.visualizar_imagen(imagen)
    original = imagen.copy()
    cv2.floodFill(imagen,None,(0,0),255)
    ArcadioCv.visualizar_imagen(imagen)
    for i in range(rows):
        for j in range(cols): 
            imagen[i,j] = 255 if imagen[i,j] == 0 else 0

    final = np.zeros((rows,cols),np.uint8)
   
    for i in range(rows):
        for j in range(cols): 
            final[i,j] = imagen[i,j] + original[i,j]
    for i in range(rows):
        for j in range(cols): 
            final[i,j] = 255 if final[i,j] == 0 else 0

    ArcadioCv.visualizar_imagen(final)
    imagen_cruces, imagen_delta,imagen_final,imagen_log = ArcadioCv.filtro_log(final,7,1)
    ArcadioCv.visualizar_imagen(imagen_final)
    

"""
    Esta función genera la segmentación por color con el algoritmo de KMEANS
    Usamos k = 4, pues dio el mejor resultado, una vez teniendo esto
    Separa en k imagenes, en este caso 4, y le aplica el filtro log a cada una,
    esta nos estaría sacando los bordes de los k objetos
"""
def segementar_imagen_por_color():
    imagen_agrupada,coordenadas = Kmeans.k_means("Jit1.jpg",4)
    cv2.imwrite('images/jit_segmentada.jpg',imagen_agrupada)
    ArcadioCv.visualizar_imagen(imagen_agrupada)
    imagenes_log = crear_imagenes(coordenadas,imagen_agrupada)
    indice = 0
    for i in imagenes_log: 
        #ya está en grises, pero para que no tenga error al guardar
        
        cv2.imwrite(f'images/Log_jit_{str(indice)}.png',i)
        indice+=1
    return imagenes_log

def binarizar(imagen):
    rows,cols = imagen.shape
    for i in range(rows):
        for j in range(cols):
            imagen[i,j] = 255 if imagen[i,j] >0 else 0
    return imagen


"""
    Esta funcion encuentra las lineas que intersectan con la imagen
    separando el objeto de todo el fondo negro, de manera que podemos visualizar
    aproximadamente los puntos en los que debemos realizar las distancias
"""
def encontrar_puntas(imagen):
    rows,cols = imagen.shape
    print(imagen.shape)
    minimo = 0
    maximo = rows-1
    bandera = False
    #el minimo es el primer punto en donde encontremos un 255
    #recorremos por columnas para el minimo
    for j in range(cols):
        for i in range(rows):
            if(imagen[i,j]==255):
                bandera = True
        if(bandera == True):
            minimo = j
            break
    #print(imagen[:,j-1]) # 
    #print(minimo)
    #encontramos el maximo
    #imagen_invertida = imagen
    for j in range(cols):
        for i in range(rows):
            if(imagen[i,j]==255):
                bandera = True
        if(bandera == True):
            #minimo = j
            break
    
    #encontramos todos los blancos 
    blancos = []
    for i in range(rows):
        for j in range(cols): 
            if(imagen[i,j]==255):
                blancos.append( [i,j] )
    blancos = np.array(blancos)
    #minimo
    imagen_nueva = imagen.copy()

   

    minimo_filas = np.min(blancos[:,1]) #donde aparece primero un 255 en filas
    maximo_filas = np.max(blancos[:,1])

    minimo_columnas = np.min(blancos[:,0]) #donde aparece primero un 255 en columnas
    maximo_columnas = np.max(blancos[:,0])


    #print("minimo",minimo_filas)

    imagen_nueva[:,minimo_filas] = 75
    imagen_nueva[:,maximo_filas] = 75

    imagen_nueva[minimo_columnas,:] = 127
    imagen_nueva[maximo_columnas,:] = 127
    ArcadioCv.visualizar_imagen(imagen_nueva)
    cv2.imwrite("images/separaciones/jit_lineas.png",imagen_nueva)
    return minimo_filas,maximo_filas,minimo_columnas,maximo_columnas
    
"""-
Funcion que encuentra la distancia y la linea en jitomates horizontales
"""
def encontrar_distancias_derecho(imagen,inicio,fin):
    rows,cols = imagen.shape
    
    #ArcadioCv.visualizar_imagen(imagen,"JITOO")
    #imagen_interseccion = imagen.copy()
    fila = imagen[:,inicio]
    #print("XD",inicio)
    x1=0
    for j in range(rows): 
        if(fila[j] == 255):
            x1=j
            i=j
            break
    fila = imagen[:,fin]
    
    x2=0
    for j in range(rows): 
        if(fila[j] == 255):
            x2 = j
            break
    
    distancia = ((x2-x1)**2+(fin-inicio)**2)**0.5
    #sacamos la recta entre 2 puntos
    #inicio y fin
    m1 = (inicio,x1,1)
    m2 = (fin,x2,1)
    
    imagen[x1,inicio] = 127

    ArcadioCv.visualizar_imagen(imagen)
    linea = Analisis2D.linea_entre_2_puntos(m1,m2)
    x,y = linea
    #ax+by+c = 0
    x = np.array(x,np.uint)
    y = np.array(y,np.uint)


    imagen[i,inicio:fin] = 127
    cv2.imwrite("images/separaciones/jito2.png",imagen)
    ArcadioCv.visualizar_imagen(imagen)
    return distancia, (i,inicio,fin)

"""
    Encuenttra la disdtancia de jitomates cuando alguno esta inclinado de alguna manera
"""
def encontrar_distancia_inclinada(imagen,minimo_filas,maximo_filas,minimo_columnas,maximo_columnas):
    #tenemos la recta x = minimo_columnas
    rows,cols = imagen.shape
    #necesitamos la interseccion de abajo a la izquierda y arriba a la derecha
    #linea de abajo con la de isquierda
    p_1 = (maximo_columnas,minimo_filas,1)
    p_2 = (minimo_columnas,maximo_filas,1)
    #sacamos la recta de los 2 puntos
    x1,y1 = Analisis2D.linea_entre_2_puntos(p_1,p_2)
    x1 = x1[19*6:len(x1)-12*6]
    y1 = y1[19*6:len(y1)-12*6]

    puntos = []
    #quitamos los que se sobresalen de la imagen, hasta que encuentre un 255 
    """ for i in range(len(x1)): 
                if(imagen[x1[i],y1[i]]==255):
                    puntos.append((x1[i],y1[i]))
   
    puntos = np.array(puntos) """
    
    distancia = ((x1[0] - x1[len(x1)-1])**2 + (y1[0] - y1[len(y1)-1])**2 )**0.5

    print(distancia)
    x1 = np.array(x1,np.uint)
    y1 = np.array(y1,np.uint)
    
    imagen[x1,y1] = 127

    cv2.imwrite("images/separaciones/jito4.png",imagen)
    
    return x1,y1,distancia

    
    ArcadioCv.visualizar_imagen(imagen)
    pass


"""
    Está función manda a llamar al Kmeans que segmenta las imagenes
    por coordenadas, es decir, separa las imagenes en donde hay blancos
    se aplica a la imagen pasada por el filtro log, pues esta nos da los bordes
"""
def separar_objetos(): 
    imagen = ArcadioCv.abrir_imagen_grises('images/Log_jit_2.png')
    imagen = binarizar(imagen)

    ArcadioCv.visualizar_imagen(imagen)
    #realizamos el kmeans a las coordenadas
    imagenes = Kmeans2D.k_means_2d(imagen,4,seed=10) #separamos los 4 jitomates
    index = 0
    for imagen in imagenes: 
        cv2.imwrite(f'images/jitomates/jitomate_{str(index+1)}.png',imagen)
        ArcadioCv.visualizar_imagen(imagen,f'Jitomate {str(index+1)}')
        index+=1
    
    return imagenes
    
"""Aqui se encontrarán las distancias mencionadas en la practica"""
def distancias():
    #jitomate 2 y jitomate 4 nos dieron los que queremos
    jitomate2 = ArcadioCv.abrir_imagen_grises('images/jitomates/jitomate_1.png') # el derech
    jitomate4 = ArcadioCv.abrir_imagen_grises('images/jitomates/jitomate_3.png') # el inclinado 

    jitomate2 = binarizar(jitomate2)
    jitomate4 = binarizar(jitomate4)

    
    #print(jitomate2)


    jitomate_bgr = cv2.imread('Jit1.jpg')
    color_linea = np.array([255,0,0],np.uint8)
    print("--------------------------JITOMATE 2-------------------------------")
    
    minimo_filas,maximo_filas,minimo_columnas,maximo_columnas = encontrar_puntas(jitomate2)
    #print("PUNTOS DE UNION EN JITOMATE 1: (",minimo_filas,maximo_filas,")")
    distancia_jito_2, recta = encontrar_distancias_derecho(jitomate2,minimo_filas,maximo_filas)
    i,inicio,fin = recta
    print("DISTANCIA DEL JITOMATE 2: ",distancia_jito_2)
    #print("DISTANCIA DEL JITOMATE 2 en imagen de dimension original: ",distancia_jito_2*6)
    #print(i,inicio,fin)
    color_linea = (255,0,0)
    jitomate_bgr[i,inicio:fin] = color_linea
    jitomate_bgr = cv2.line(jitomate_bgr, (inicio,i), (fin,i), color_linea, 9)
    
    print("--------------------------------------------------------------------")
    print("--------------------------JITOMATE 4-------------------------------")

    minimo_filas,maximo_filas,minimo_columnas,maximo_columnas  = encontrar_puntas(jitomate4)
    x1,y1,distancia_jito_4 = encontrar_distancia_inclinada(jitomate4,minimo_filas,maximo_filas,minimo_columnas,maximo_columnas)
    print("PUNTOS JITOMATE 4: ",(y1[0],x1[0]),(y1[len(y1)-1],x1[len(x1)-1]))
    print("DISTANCIA DEL JITOMATE 4: ",distancia_jito_4)
    #print("DISTANCIA DEL JITOMATE 4 en imagen de dimension original: ",distancia_jito_4*6)
    print("--------------------------------------------------------------------")
    jitomate_bgr[x1,y1] = color_linea
    color_linea = (255,0,0)

    jitomate_bgr = cv2.line(jitomate_bgr, (y1[0],x1[0]), (y1[len(y1)-1],x1[len(x1)-1]), color_linea, 9)

    cv2.imshow("IMAGEN FINAL ",jitomate_bgr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    cv2.imwrite('images/resultados/imagen_escala_6.png',jitomate_bgr)


    
if __name__ == "__main__":
    #segmentamos
    segmentadas = segementar_imagen_por_color()
    #separamos los objttos de la imagen
    #fill()
    separar_objetos()
    distancias()

    
    
    
