from ArcadioCv import * 
from Kmeans import * 
from Kmeans2D import * 
import cv2

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

def separar_objetos(): 
    imagen = ArcadioCv.abrir_imagen_grises('images/Log_jit_2.png')
    rows,cols = imagen.shape
    for i in range(rows):
        for j in range(cols):
            imagen[i,j] = 255 if imagen[i,j] >0 else 0

    ArcadioCv.visualizar_imagen(imagen)
    #realizamos el kmeans a las coordenadas
    imagenes = Kmeans2D.k_means_2d(imagen,4) #separamos los 4 jitomates
    index = 0
    for imagen in imagenes: 
        cv2.imwrite(f'images/jitomates/jitomate_{str(index+1)}.png',imagen)
        index+=1




if __name__ == "__main__":
    #segmentamos
    segmentadas = segementar_imagen_por_color()
    #separamos los objttos de la imagen
    separar_objetos()

    
    
    