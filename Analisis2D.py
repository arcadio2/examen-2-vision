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

    def interseccion_lineas(l1,l2):
        a1,b1,c1 = l1
        a2,b2,c2 = l2
      
        print(f'Linea 1: {str(a1)}x + {str(b1)}y +{str(c1)} ')
        print(f'Linea 2: {str(a2)}x + {str(b2)}y +{str(c2)} ')

        x,y,z = Analisis2D.producto_cruz(l1,l2)
        #print(x,y,z)
        #ax+by+z=0, y = -z/
        
        """  x1,y1 = Analisis2D.puntos_lineas(a1,b1,1)
        x2,y2 = Analisis2D.puntos_lineas(a2,b2,1)
        plt.title("Intersección de dos rectas")
        plt.plot(x1,y1)
        plt.plot(x2,y2)
        plt.scatter(x,y,s=30,c="red") """
        

        plt.show()
        return (x,y,z)
    
    def linea_entre_2_puntos(m1,m2):
        a1,b1,c1 = m1
        a2,b2,c2 = m2


        m1 = (a1,b1,1)
        m2 = (a2,b2,1)
        x,y,z = Analisis2D.producto_cruz(m1,m2)
        x1,y1 = Analisis2D.puntos_lineas(x,y,1,a1+1,a2,1)
        #print(x1,y1)
        print("PUNTO 1 (",a1,b1,1,")")
        print("PUNTO 2 (",a2,b2,1,")")

        plt.title("Recta entre 2 puntos")
        plt.plot(x1,y1)
        plt.scatter(a1,b1,s=30,c="red")
        plt.scatter(a2,b2,s=30,c="red")

        plt.show()
        return (x1,y1)
    
    def distancia_2_puntos(l1,l2,l3): 
        a1,b1,c1 = l1
        a2,b2,c2 = l2
        a3,b3,c3 = l3

        print(f'Linea 1: {str(a1)}x + {str(b1)}y +{str(c1)} ')
        print(f'Linea 2: {str(a2)}x + {str(b2)}y +{str(c2)} ')
        print(f'Linea 3: {str(a3)}x + {str(b3)}y +{str(c3)} ')

        l3 = (a3,b3,1)

        m1 = Analisis2D.producto_cruz(l1,l3)
        m2 = Analisis2D.producto_cruz(l2,l3)

        x1,y1,z1 = m1
        x2,y2,z2 = m2

        """ print("PUNTO 1 (",x1,y1,z1,")")
        print("PUNTO 2 (",x2,y2,z2,")") """

        distancia = ( (x2-x1)**2 + (y2-y1)**2 )**0.5
        
        x_line_1,y_line_1 = Analisis2D.puntos_lineas(a1,b1,1)
        x_line_2,y_line_2 = Analisis2D.puntos_lineas(a2,b2,1)
        x_line_3,y_line_3 = Analisis2D.puntos_lineas(a3,b3,1)

        plt.plot(x_line_1,y_line_1)
        plt.plot(x_line_2,y_line_2)
        plt.plot(x_line_3,y_line_3)

        plt.scatter(x1,y1,s=30,c="red")
        plt.scatter(x2,y2,s=30,c="red")
        plt.show()
        print("-----------------------------------------------")
        print("PUNTO 1",m1)
        print("PUNTO 2",m2)
        print("La distancia es: ",distancia)
        print("-----------------------------------------------")