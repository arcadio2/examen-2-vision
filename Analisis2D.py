import numpy as np
from ArcadioCv import *

class Analisis2D: 
    def producto_cruz(p1,p2):
        a1,b1,c1 = p1
        a2,b2,c2 = p2

        x = b1*1 - b2*1 #c2,c1
        y = -(a1*1-a2*1)
        z = a1*b2 - a2*b1
        #normalizamos el vector
        x = x/z if z != 0 else 0
        y = y/z if z != 0 else 0
        z = z/z if z != 0 else 0
        #retornamos el vector
        return (x,y,z)

    def puntos_lineas(a,b,c,inicio=-100,final=100,saltos=10):
        x = np.array(range(inicio,final))/saltos
        if(inicio>final):
            x = np.array(range(final,inicio))/saltos
        #0 = ax +by +z
        y = (-c-a*x)/b 
        return (list(x),list(y))

    def interseccion_lineas(l1,l2,imagen):
        a1,b1,c1 = l1
        a2,b2,c2 = l2
      
        print(f'Linea 1: {str(a1)}x + {str(b1)}y +{str(c1)} ')
        print(f'Linea 2: {str(a2)}x + {str(b2)}y +{str(c2)} ')

        x,y,z = Analisis2D.producto_cruz(l1,l2)
        print(x,y,z)
        #ax+by+z=0, y = -z/
        
        x1,y1 = Analisis2D.puntos_lineas(a1,b1,1)
        x2,y2 = Analisis2D.puntos_lineas(a2,b2,1)
        plt.title("Intersección de dos rectas")
        plt.plot(x1,y1)
        plt.plot(x2,y2)
        plt.scatter(x,y,s=30,c="red")

        plt.show()
    
    def linea_entre_2_puntos(m1,m2,imagen):
        a1,b1,c1 = m1
        a2,b2,c2 = m2

        print("Seleccione las cooordenadas del punto 1")
        a1 = int(input("Ingrese a1: "))
        b1 = int(input("Ingrese b1: "))
        c1 = 1

        print("Seleccione las cooordenadas del punto 2")
        a2 = int(input("Ingrese a2: "))
        b2 = int(input("Ingrese b2: "))
        c2 = 1

        m1 = (a1,b1,1)
        m2 = (a2,b2,1)
        x,y,z = Analisis2D.producto_cruz(m1,m2)
        x1,y1 = Analisis2D.puntos_lineas(x,y,1,a1,a2+1,1)
        print(x1,y1)
        print("PUNTO 1 (",a1,b1,1,")")
        print("PUNTO 2 (",a2,b2,1,")")

        plt.title("Recta entre 2 puntos")
        plt.plot(x1,y1)
        plt.scatter(a1,b1,s=30,c="red")
        plt.scatter(a2,b2,s=30,c="red")

        plt.show()