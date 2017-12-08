class Biblioteca():
    def __init__(self):
        print("Hola")
    def argumentos_validos(self,funcion,num, texto):
        ms = texto.strip() #quitamos los espacios en blanco
        print("Función:"+funcion)
        print("Texto:"+ms)
        if(ms.find(funcion)==-1): #busco el texto de la función a usar
            return False
        else:
            print("Entro")
            ms = ms.split(" ")
            count_ms = len(ms)
            print("mensaje:",count_ms,"numero:",num)
            if(count_ms == num):
                mi_array = []
                for num in range(0,count_ms):
                    mi_array.append(ms[num])
                    print(num)

                return mi_array
            else:
                print("Expresión mal argumentada")
                return False

if __name__ == "__main__":
    message = "shodan apache 5"
    b = biblioteca()
    a = b.argumentos_validos("shodan",3,message)
    print(a)
