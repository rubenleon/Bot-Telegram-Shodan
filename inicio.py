import time
import requests
import telebot #Importamos las librería
from telebot import types
#import sys
#import os
#import string
#import math

#LIBRERIAS PROPIAS
from biblioteca import Biblioteca
from ishodan import Info_Shodan
from class_log import Log

def teclado_tl(num):
	markup = types.ReplyKeyboardMarkup(row_width=5)

	mi_array = []
	for i in range(1,num+1):
		mi_array.append(types.KeyboardButton(i))

	#num_teclado = math.ceil(num)
	#num_teclado2 = math.floor(num)
	#print("Teclado numero: "+str(num_teclado))
	#print("Teclado numero: "+str(num_teclado2))

	#for i in range(0,num_teclado):
	#print(type(markup))
	#print("Array:"+str(mi_array[0]))

	markup.add(*mi_array)
	#markup.add(mi_array[1])
	#markup.add(mi_array[2])

	itembtncancelar = types.KeyboardButton('cancelar')
	markup.row(itembtncancelar)
	return markup

def quitar_teclado(object,chat_id):
	markup = types.ReplyKeyboardRemove(selective=False)
	bot.send_message(chat_id, "CANCELAR", reply_markup=markup)

TOKEN = open('telegram-key.txt').readline().rstrip('\n') # Ponemos nuestro Token generado con el @BotFather

bot = telebot.TeleBot(TOKEN) # Combinamos la declaración del Token con la función de la API
diccionario_shodan = None

@bot.message_handler(func=lambda message: True)
def echo_all(message):

	l = Log("log/")

	chat_id = message.from_user.id

	if(message.text.isdigit()):
		if(int(message.text) >=1 and int(message.text) <=20):
			#print("Prueba")
			global diccionario_shodan
			print(diccionario_shodan)
			print("Tamaño diccionario: ",len(diccionario_shodan))
			if(diccionario_shodan == None):
				quitar_teclado(bot,chat_id)
			else:
				print("Numero: ",message.text)
				dict_shodan = diccionario_shodan
				#dict_shodan = diccionario_shodan
				print("Diccionario Shodan",dict_shodan)
				bot.send_message(chat_id,dict_shodan,parse_mode="HTML")
		else:
			print("Lo siento") # Sin implementar

	if(message.text.find("shodan")!=-1):
		sms = message.text
		bi = Biblioteca()
		argumentos = bi.argumentos_validos("shodan",2,sms)
		if argumentos==False:
			cadena="<b>SHODAN: </b>Shodan es un motor de búsqueda que le permite al usuario encontrar iguales o diferentes tipos específicos de equipos (routers, servidores, etc.) conectados a Internet a través de una variedad de filtros.\n"
			cadena+="\n<b>Ejemplos de uso:</b>\n\n<code>shodan 'búsqueda' 'número de búsquedas'</code>\n\n<code>shodan apache</code>\n<code>shodan apache 5</code>\n"
			cadena+="<code>shodan apache 20</code>.\n\nNota: <b>20</b> es el número máximo de busquedas"
			#cadena ="<b>Ejemplos de uso</b>"
			bot.send_message(chat_id,cadena,parse_mode="HTML")
		else:
			print(argumentos)

			i = Info_Shodan()
			res = i.buscar(argumentos[1])
			resultados = i.nlimit

			if(res==True):
				array_tl = i.datos_telegram()
				#n_array_tl = len(array_tl)
				#print("n_array_tl: ",n_array_tl)

				markup = teclado_tl(resultados)
				l.log("markup generado.")

				for datos_tl in array_tl:
					#print("Diccionario IP: ",i.diccionario_ip)
					#print()
					bot.send_message(chat_id,datos_tl,parse_mode="HTML")

				#global diccionario_shodan
				diccionario_shodan = i.diccionario_ip

				bot.send_message(chat_id,"<b>Elige una opción (1/"+str(resultados)+"): </b>",parse_mode="HTML",reply_markup=markup)

			elif(res==False):
					bot.send_message(chat_id,"No hay ningún resultado con la buscada: <b>"+str(argumentos[1]+"</b>"),parse_mode="HTML")
			else:
				bot.send_message(chat_id,res,parse_mode="HTML")

	elif message.text == "/a":
		markup = teclado_tl(20)
		bot.send_message(chat_id, "Elige una opción:", reply_markup=markup)

	elif message.text == "/autor":
		texto = "Autor: Rubén León"
		texto+= "Github: "
		bot.send_message(chat_id, texto)

	elif message.text == "cancelar":
		#from telebot import types
		#markup = types.ReplyKeyboardHide(selective=False)
		markup = types.ReplyKeyboardRemove(selective=False)
		bot.send_message(chat_id, "CANCELAR", reply_markup=markup)

		#bot.send_message(chat_id, "CANCELAR", reply_markup=markup)

	#print(message)
	id_tele = str(message.from_user.id)
	nombre = str(message.from_user.first_name)
	apellido = str(message.from_user.last_name)
	mensaje = str(message.text)

	print("")
	print("ID: "+id_tele) #id de usuario
	print("Nombre: "+nombre) #Nombre de usuario
	print("Apellido: "+apellido) #Apellido de usuario
	print("Mensaje: "+mensaje) #Mensaje
	print("")

	l.log("ID:"+id_tele+"-Nombre:"+nombre+"-Apellido:"+apellido+"-Mensaje:"+mensaje)


def inicializar_bot():
	l = Log("log/")
	l.logp("Arranque del Bot")
	try:
		bot.polling(True,False,True)
	except requests.exceptions.ReadTimeout:
		print("Timeout occurred")
		l.log("Timeout occurred")
		time.sleep(2)
		print("Pausa de 2 segundo")
		l.log("Pausa de 2 segundo")
		inicializar_bot()
	except requests.exceptions.ConnectionError:
		print("Error en la conexión")
		l.log("Error en la conexión")
		time.sleep(2)
		print("Pausa de 2 segundo")
		l.log("Pausa de 2 segundo")
		inicializar_bot()
		#print(except)

inicializar_bot()
