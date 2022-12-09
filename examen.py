from ArcadioCv import * 
from Kmeans import * 
from Kmeans2D import * 
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
    for imagen in imagenes:
        #grises = ArcadioCv.rgb_to_grises(imagen)
        imagen_cruces, imagen_delta,imagen_final,imagen_log = ArcadioCv.filtro_log(imagen,5,1)
        ArcadioCv.visualizar_imagen(imagen_log)
        imagenes_log.append(imagen_log)
    return imagenes_log

"""
    Esta función genera la segmentación por color con el algoritmo de KMEANS
    Usamos k = 4, pues dio el mejor resultado, una vez teniendo esto
    Separa en k imagenes, en este caso 4, y le aplica el filtro log a cada una,
    esta nos estaría sacando los bordes de los k objetos
"""
def segementar_imagen_por_color():
    imagen_agrupada,coordenadas = Kmeans.k_means("jit3.jpg",4)
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
    print(imagen[:,j-1]) # 
    print(minimo)
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
    minimo_filas = np.min(blancos[:,1]) #donde aparece primero un 255 en columnas
    maximo_filas = np.max(blancos[:,1])

    minimo_columnas = np.min(blancos[:,0]) #donde aparece primero un 255 en columnas
    maximo_columnas = np.max(blancos[:,0])
    print("minimo",minimo_filas)
    imagen[:,minimo_filas] = 75
    imagen[:,maximo_filas] = 75

    imagen[minimo_columnas,:] = 127
    imagen[maximo_columnas,:] = 127


    ArcadioCv.visualizar_imagen(imagen)

    


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
    imagenes = Kmeans2D.k_means_2d(imagen,4,seed=1) #separamos los 4 jitomates
    index = 0
    for imagen in imagenes: 
        cv2.imwrite(f'images/jitomates/jitomate_{str(index+1)}.png',imagen)
        ArcadioCv.visualizar_imagen(imagen,f'Jitomate {str(index+1)}')
        index+=1
    
    return imagenes
    
"""Aqui se encontrarán las distancias mencionadas en la practica"""
def distancias():
    #jitomate 2 y jitomate 4 nos dieron los que queremos
    jitomate2 = ArcadioCv.abrir_imagen_grises('images/jitomates/jitomate_2.png')
    jitomate4 = ArcadioCv.abrir_imagen_grises('images/jitomates/jitomate_4.png')

    jitomate2 = binarizar(jitomate2)
    jitomate4 = binarizar(jitomate4)

    print(jitomate2)

    encontrar_puntas(jitomate2)
    encontrar_puntas(jitomate4)

    
if __name__ == "__main__":
    #segmentamos
    #segmentadas = segementar_imagen_por_color()
    #separamos los objttos de la imagen
    #separar_objetos()
    distancias()

    
    
    