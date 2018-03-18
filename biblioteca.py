class Biblioteca():
    def argumentos_validos(self,texto):
        texto = texto.strip() #quitamos los espacios en blanco
        texto = texto.lower()

        if(texto!=None and texto!=""):
            texto = texto.split(" ")

            n = len(texto)

            if(n==2):
                if(texto[0] == "shodan"):
                    return {"n":10,"busqueda":texto[1]} #Devolvemos un diccionario con n por defecto a 10
                else:
                    return "No has escrito 'shodan' en la instrucción."
            elif(n==3):
                if(texto[0] == "shodan"):
                    if(texto[2].isdigit()):
                        return {"n":int(texto[2]),"busqueda":texto[1]}
                    else:
                        return "El tercer valor tiene que ser un etero."
                else:
                    return "No has escrito 'shodan' en la instrucción."
            else:
                return False
        else:
            return "No has escrito ninguna instrucción"

if __name__ == "__main__":
    b = Biblioteca()
    #res = b.argumentos_validos("shodan apache 5")
    res = b.argumentos_validos("shodan apache 5")
    if type(res) is dict:
        print("Es un diccionario")
    print(res)
