import time

class Log():
    def __init__(self,ruta=""):
        self.f = None #Fichero donde se guardan los LOG del Bot
        if(ruta == "" or ruta == None):
            self.ruta = ""
        else:
            self.ruta = ruta

    def get_nombre_fichero(self):
        fecha = time.strftime("%Y-%m-%d")
        return fecha #Nombre del fichero

    def get_fecha_hora_log(self):
        hora = time.strftime("%H:%M:%S")
        fecha = time.strftime("%d-%m-%Y")
        return fecha+" "+hora+" - " #Nombre del fichero


    def abrir_f(self,tipo): #Tipo tiene dos valores: l => fichero de log y e => fichero de error
        nombre = self.get_nombre_fichero()
        if(tipo=="l"): #creamos un fichero para el LOG del BOT
            self.f = open(self.ruta+nombre+"-log.txt","a")
        else: #creamos un fichero para los errores del bot
            self.f = open(self.ruta+nombre+"-error.txt","a")

    def cerrar_f(self):
        self.f.close()

    def write(self,texto,tipo):
        self.abrir_f(tipo)
        self.f.write(self.get_fecha_hora_log()+texto+"\n")
        self.cerrar_f()

    def log(self,texto):
        self.write(texto,"l")

    def logp(self,texto):
        print(texto)
        self.log(texto)

    def error(self,texto):
        self.write(texto,"e")

if __name__ == "__main__":
    print("Primero prueba")
    l = Log("log/")
    l.log("Prueba")
    l.log("Prueba2")
    l.log("Prueba3")
    l.error("Prueba4")
    l.log("Prueba5")
    l.log("Prueba6")
