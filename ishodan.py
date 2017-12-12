#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shodan
from class_log import Log

class Info_Shodan():
    def __init__(self):
        self.l = Log("log/")
        self.key = open('shodan-key.txt').readline().rstrip('\n')
        self.api = shodan.Shodan(self.key)
        self.resultado_total = None
        self.resultado_matches = None
        self.l.logp("INICIO")

    def buscar(self,busqueda,nlimit=10):
        try:
            # Buscamos en Shodan con el método WebAPI.search()
            self.l.logp("Buscando '"+busqueda+"' en ishodan ... ")
            resultados = self.api.search(busqueda,limit=nlimit)
            #resultados = self.api.search('proconsi',limit=15)
            self.l.logp("Resultados totales de Shodan: "+str(resultados['total']))
            self.l.logp("Fin de la Búsqueda")


            ################################################################################
            # Obtneer resultado
            self.resultado_total = resultados['total'] #Resultado total en la BBDD de Shodan
            self.nlimit = nlimit #Número de resultado maximo de telegram

            if(self.resultado_total < self.nlimit):
                self.nlimit = self.resultado_total
            ################################################################################

            if self.resultado_total == 0:
                return False

            self.resultado_matches = resultados['matches']
            return True

        except shodan.APIError as e:
            self.l.logp('Error ishodan: %s' % e)
            return('Error ishodan: %s' % e)

    def host(self,ip):
        host = self.api.host(ip)
        print(host)
        print()
        print()
        print()

        for c,item in enumerate(host['data']):
            print(str(c)+" OTRO ... \n")
            print(item)
            print()
        exit()

        # Print general info

        print ('IP: %s ' % host['ip_str'])
        print ('Organizacion: %s ' % host.get('org', 'n/a'))
        print ('Sistema operativo: %s ' % host.get('os', 'n/a'))
        for item in host['data']:
            print ('Puerto: %s ' % item['port'])
            print ('Banner: %s ' % item['data'])

    def pantalla(self):
        for i in self.resultado_matches:
            print(i)
            exit()
            print ('IP: %s' % i['ip_str'])
            print ('Data: %s' % i['data'])
            print ('Hostnames: %s' % i['hostnames'])
            print ('Puerto: %s' % i['port'])
            print ('')

    def datos_telegram_location(self,location):
        texto = "\n"
        log = 0.0
        lat = 0.0
        texto+="<strong>Location</strong>: \n"
        if(location['city'] != None):
            texto+="\t\t\t<strong>City</strong>: "+str(location['city'])+"\n"

        if(location['country_code'] != None):
            texto+="\t\t\t<strong>country_code</strong>: "+str(location['country_code'])+"\n"

        if(location['country_name'] != None):
            texto+="\t\t\t<strong>country_name</strong>: "+str(location['country_name'])+"\n"

        if(location['area_code'] != None):
            texto+="\t\t\t<strong>area_code</strong>: "+str(location['area_code'])+"\n"

        if(location['longitude'] != None):
            texto+="\t\t\t<strong>longitude</strong>: "+str(location['longitude'])+"\n"

        if(location['latitude'] != None):
            texto+="\t\t\t<strong>latitude</strong>: "+str(location['latitude'])+"\n"

        if(location['postal_code'] != None):
            texto+="\t\t\t<strong>postal_code</strong>: "+str(location['postal_code'])+"\n"

        texto+= "\n"
        return texto

    def datos_telegram(self):
        mi_array = [] #array para guardar el resultado de cada consulta

        #diccionario para saber la ip por el número de la consulta
        self.diccionario_ip = {}

        cont = 1
        for i in self.resultado_matches:
            texto = "<strong>"+str(cont)+")</strong>\n\n"
            texto+=("<strong>IP:</strong> %s\n" % i['ip_str'])

            #añadimos valor al diccionario_ip
            self.diccionario_ip[cont] = i['ip_str']

            #texto+=("<strong>Modulo:</strong> %s\n" % i['module'])
            texto+=("<strong>ISP:</strong> %s\n" % i['isp'])

            texto+=("<strong>Hostnames:</strong> %s\n" % i['hostnames'])
            texto+=("<strong>Puerto:</strong> %s\n" % i['port'])

            texto+=self.datos_telegram_location(i['location'])

            data = i['data']
            n_data_len = len(data)
            if(n_data_len >= 100):
                data = data[0:100]
            #print("logitud: ",len(data))
            #exit()
            texto+=("<strong>Data:</strong><code>\n%s\n</code>" % data)
            texto+=('')
            cont=cont+1
            #print(i)
            #exit()
            mi_array.append(texto)
        return mi_array

if __name__ == "__main__":
    print("Ejemplo")
    i = Info_Shodan()
    #res = i.host("41.142.245.134")
    res = i.host("88.20.94.195")
    #if(res==True):
    #    print(i.datos_telegram())
    #else:
    #    print(res)
