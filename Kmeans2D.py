from ArcadioCv import * 
import random
import numpy as np 
import math 


"""
Esta clase hace un KMEANS en 2D, esto es para las coordenadas de la imagen
y saber donde están agrupados los objetos
"""
class Kmeans2D:

    def distancia_euclidiana(d1,d2):
        x0=d1[0]
        x1=d2[0]
        y0=d1[1]
        y1=d2[1]
        return ((x1-x0)**2+(y1-y0)**2)**0.5

    def k_aleatorios(k,puntos):
        lista = []
        for i in range(k): 
            #en los rangos de la imagen
            x = random.choice(puntos)
            y = random.choice(puntos)
            #coords = (x,y)
            lista.append(x)
        return lista
    
    def obtener_k(vectores):
        x=[]
        y=[]
        
        for vector in vectores:
            x.append(vector[0])
            y.append(vector[1])
        mean_x = np.mean(x)
        mean_y= np.mean(y)
        return (mean_x,mean_y)

    def redefinir_k(agrupaciones): 
        new_k_points = []
        for group in agrupaciones: 
            valores = group.get('indices')
            new_point = Kmeans2D.obtener_k(valores)
            if(math.isnan(new_point[0]) ):
                print("xd")
                new_point = group.get('k_point')

            new_k_points.append(new_point)
            
        return new_k_points
    
    def agrupamiento(k_points,x,y): 
        k_agrupados = []
        indices = [[] for i in range(len(k_points))]
        for i in range(len(x)): 
            distancias = []
            for k in k_points: 
                distancia = Kmeans2D.distancia_euclidiana((x[i],y[i]),k)
                distancias.append(distancia)
            distancias = np.array(distancias)
            indice = np.where(distancias == np.amin(distancias))[0][0] #indice de distancia minima
            distancia_minima = distancias[indice] #encontramos la distancia minima
            
            indices[indice].append((x[i],y[i]))
        
        #print(indices[1])
        for i in range(len(k_points)):
            k_agrupados.append(
                {
                    'k_point':k_points[i],
                    "indices":indices[i],
                }
            )
        return k_agrupados
        
    def obtener_blancos(imagen):
        x = []
        y = []
        puntos = []
        rows,cols = imagen.shape
        for i in range(rows):
            for j in range(cols):
                if(imagen[i,j]==255):
                    x.append(i)
                    y.append(j)
                    puntos.append( (i,j) )
        return x,y,puntos 
    
    """
        Genera el K-means con las coordenadas de una imagen, solo donde hay blancos
    """
    def k_means_2d(imagen,K=2,seed=0):
        rows,cols = imagen.shape
        random.seed(seed)
        x,y,puntos = Kmeans2D.obtener_blancos(imagen)
        #print(puntos)
        k_points = Kmeans2D.k_aleatorios(K,puntos)
        #k_points = [(0,0),(0,cols-1),(rows,cols),(rows,0)]
        k = [(55.69138868548982, 51.73827562233507, 49.23192340328793), 
            (124.60188597303191, 122.55061319156516, 121.47310002596444), 
            (142.24691703333525, 36.51620118686638, 30.089892072925753), 
            (178.0056625814884, 183.3840251668077, 185.15679651573248)]
        k_anterior = []
        agrupaciones = Kmeans2D.agrupamiento(k_points,x,y)

        
        print("K1",k_points)
        while(k_points != k_anterior):
            k_anterior = k_points
            k_points = Kmeans2D.redefinir_k(agrupaciones)
            print(k_points)
            agrupaciones = Kmeans2D.agrupamiento(k_points,x,y)
       
        imagenes = Kmeans2D.separar_imagenes(agrupaciones,imagen)
        return imagenes

    """
        Separa cada objeto de la imagen con respecto a los centroides obtenidos
    """    
    def separar_imagenes(agrupaciones,imagen):
        rows,cols = imagen.shape
        imagenes = []
        for group in agrupaciones:
            imagen = np.zeros((rows,cols),np.uint8)
            indices = group.get('indices')
            
            for indice in indices:
                i = indice[0]
                j = indice[1]
                if(indice == (i,j)):
                    #print("xdxd")
                    #guardamos el valor
                    imagen[i,j] = 255
            imagenes.append(imagen)

        """ for imagen in imagenes:
            ArcadioCv.visualizar_imagen(imagen) """
        return imagenes

    """
        Esta función ya no se usa, pero segmenta los objetos de manera 
        vertical
    """
    def separacion_vertical(imagen):
        rows,cols = imagen.shape
        #recorremos todas las filas y luego vemos si en cualquier punto de la columna hay un blanco,
        #si hay un blanco sigue, sino acaba y separa
        #for i in range(rows)
        imagenes = []
        bandera = False
        indices = []
        imagen_nueva = np.zeros(imagen.shape,np.uint8)
        for i in range(cols): 
            #print(imagen[i,:])
            suma = np.sum(imagen[:,i])
            if(suma !=0 ):
                indices.append(i)#indices de las filas
                bandera = True

            if(bandera==True): #si encontro algun blanco en la columna
                imagen_nueva[:,i] = imagen[:,i]
            else: 
                if( np.sum(imagen_nueva)!=0): #si si ha agregado algo
                    imagenes.append(imagen_nueva)
                    imagen_nueva = np.zeros(imagen.shape,np.uint8)

            bandera = False

        print("LONGITUD",len(imagenes))
        for imagen in imagenes: 
            ArcadioCv.visualizar_imagen(imagen)
        return imagenes
            
    """
        Esta función ya no se usa, pero segmenta los objetos de manera 
        horizontal
    """
    def separacion_horizontal(imagen):
        rows,cols = imagen.shape
        imagenes = []
        bandera = False
        indices = []
        imagen_nueva = np.zeros(imagen.shape,np.uint8)
        for i in range(rows): 
            suma = np.sum(imagen[i,:])
            if(suma !=0 ):
                indices.append(i)#indices de las filas
                bandera = True

            if(bandera==True): #si encontro algun blanco en la columna
                imagen_nueva[i,:] = imagen[i,:]
            else: 
                if( np.sum(imagen_nueva)!=0): #si si ha agregado algo
                    imagenes.append(imagen_nueva)
                    imagen_nueva = np.zeros(imagen.shape,np.uint8)

            bandera = False

        print("LONGITUD",len(imagenes))
        for imagen in imagenes: 
            ArcadioCv.visualizar_imagen(imagen)
        return imagenes

    """"
        Esta oobtiene los segmentos horizontales, los verticales
        y a estos les hace un and, e ignora todos los que quedaron 
        completamente negros
    """
    def separacion_lineas(imagen):
        rows,cols = imagen.shape
        imagenes = []
        horizontales = Kmeans2D.separacion_horizontal(imagen)
        #for horizontal in horizontales:
        verticales = Kmeans2D.separacion_vertical(imagen)

        for h in horizontales:
            for v in verticales: 
                img = cv2.bitwise_and(h,v)
                if(np.sum(img)!=0):
                    imagenes.append(img)

        #imagenes = imagenes + verticales
        for imagen in imagenes: 
            ArcadioCv.visualizar_imagen(imagen)
        

if __name__ == "__main__":
    grises = ArcadioCv.abrir_imagen_grises('jit3.jpg')#cosas.webp
    imagen_cruces, imagen_delta,imagen_final,imagen_log = ArcadioCv.filtro_log(grises,5,1)
    ArcadioCv.visualizar_imagen(imagen_final,"cruces")
    #width = int(imagen_final.shape[1] * 150 / 100)
    #height = int(imagen_final.shape[0] * 150 / 100)
    #dsize = (width, height)
    #imagen_final = cv2.resize(imagen_final, dsize)
    print(imagen_final[7,:])
    random.seed(0)
    #umbral = ArcadioCv.umbral_otsu(imagen_cruces)
    #print(umbral)
    #imagen_delta = ArcadioCv.umbralar(imagen_delta,2)
    #ArcadioCv.visualizar_imagen(imagen_delta,"u")

    #ArcadioCv.visualizar_imagen(imagen_cruces)
    #ArcadioCv.visualizar_imagen(imagen_delta)
    #ArcadioCv.visualizar_imagen(imagen_log)
    Kmeans2D.separacion_lineas(imagen_final)
    #Kmeans2D.k_means_2d(imagen_final,7)