

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
