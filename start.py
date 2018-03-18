import time
import requests
import telebot #Importamos las librería
from telebot import types
import os.path as path #importamos la líbreria para comprobar si existe la BBDD
import os
import sqlite3 #Libreria para atarcar un .db

#LIBRERIAS PROPIAS
from biblioteca import Biblioteca
from ishodan import Info_Shodan

#os.system("clear")

############################################################
#########               BASE DE DATOS             ##########
############################################################

def guardar_usuario_BBDD(token,busqueda,idtg):
	conexion = sqlite3.connect('usuarios.db') # Nos conectamos a la base de datos usuarios.db (la crea si no existe)
	cursor = conexion.cursor() # Ahora crearemos una tabla de usuarios para almacenar "id", "mensaje" y "token de ip"
	cursor.execute("INSERT INTO usuarios VALUES (null,'{}', '{}', '{}')".format(idtg,busqueda,token))
	conexion.commit() # Guardamos los cambios haciendo un commit
	conexion.close() # Cerramos la conexións

def eliminar_usuario_BBDD(idtg):
	conexion = sqlite3.connect('usuarios.db')
	cursor = conexion.cursor()
	sql = "DELETE FROM usuarios WHERE idtg='{}'".format(idtg)
	print("sql borrar: ",sql)
	r = cursor.execute(sql)
	print("r:",r)
	conexion.commit()
	conexion.close()

def obtener_usuario_BBDD(idtg):
	conexion = sqlite3.connect('usuarios.db')
	cursor = conexion.cursor()

	sql = "SELECT * FROM usuarios WHERE idtg='{}'".format(idtg)
	#print("sql: ",sql)
	cursor.execute(sql) # Recuperamos un registro de la tabla de usuarios
	usuario = cursor.fetchone()
	if(usuario == None):
		#print("No hay ningun registro de este usuario")
		conexion.close()
		return False
	else:
		#print("Se han encontrado un historia de este usuario:",usuario)
		conexion.close()
		return usuario

def generar_array_key_token_BBDD(token):

	ips = token.split(",") #parto el array por la coma
	#print("ips: ", ips)
	token_array = []
	for ip in ips:
		ip_split = ip.split("=") #parto el array por el igual
		diccionario = {'cont':ip_split[0],'ip':ip_split[1]} #creo un diccionario
		token_array.append(diccionario) #creo un array de diccionarios

	#print("Token_array: ",token_array)

	return token_array #Devolvemos un array

############################################################
#########           END BASE DE DATOS             ##########
############################################################



############################################################
#########           FUNCIONES BOT                 ##########
############################################################

def crear_teclado_tl(num):
	markup = types.ReplyKeyboardMarkup(row_width=5)

	mi_array = []
	for i in range(1,num+1):
		mi_array.append(types.KeyboardButton(i)) #creación de botones numericos

	markup.add(*mi_array)

	itembtncancelar = types.KeyboardButton('cancelar')
	markup.row(itembtncancelar) #creación de botón cancelar
	return markup

def obtener_numero_teclado(message):
	if(int(message.text) >=1 and int(message.text) <=20):
		usuario = obtener_usuario_BBDD(message.from_user.id)
		token = usuario[3]
		array_token = generar_array_key_token_BBDD(token)

		indice = int(message.text)-1
		valor = array_token[indice]['ip']
		print("valor:",valor)
		return str(valor)

	else:
		return "Lo siento, tiene que ser un número del 1 al 20"

############################################################
#########           END FUNCIONES BOT             ##########
############################################################

TOKEN = open('telegram-key.txt').readline().rstrip('\n') # Ponemos nuestro Token generado con el @BotFather
bot = telebot.TeleBot(TOKEN) # Combinamos la declaración del Token con la función de la API
i = Info_Shodan() #Inicializo la Clase Info_Shodan()

##Comprobamos si existe la BBDD, sino creamos la BBDD##
if path.isfile("usuarios.db") != True:
	print("Creamos Base de datos de usuarios")

	conexion = sqlite3.connect('usuarios.db') # Nos conectamos a la base de datos usuarios.db (la crea si no existe)
	cursor = conexion.cursor() # Ahora crearemos una tabla de usuarios para almacenar "id", "mensaje" y "token de ip"
	cursor.execute("CREATE TABLE usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT,idtg VARCHAR(100),mensaje VARCHAR(100), tokenip VARCHAR(250))")
	conexion.commit() # Guardamos los cambios haciendo un commit

	#cursor.execute("INSERT INTO usuarios VALUES (null,'188396571', 'apache 5', '1=192.168.1.211,2=192.168.1.209')")

	conexion.commit() # Guardamos los cambios haciendo un commit
	conexion.close() # Cerramos la conexións


@bot.message_handler(func=lambda message: True)
def echo_all(message):

	chat_id = message.from_user.id #ID único de Telegram

	if(obtener_usuario_BBDD(chat_id)!=False):
		print("Se encontro el usuario '{}' en la BBDD".format(chat_id))

		if(message.text.isdigit()):
			ip = obtener_numero_teclado(message)
			if(ip!=False):
				print("Mostramos toda la info que nos da Shodan",ip)
				print()
				cadena = i.host(ip)
				print("dad")
				bot.send_message(chat_id,cadena,parse_mode="HTML")

				posicion=i.localizacion()
				if(posicion!=False):
					print("Posición:",posicion)
					lat_log = posicion.split(";") #parto el array por el igual
					lat=float(lat_log[0])
					log=float(lat_log[1])

					bot.send_location(chat_id, lat, log)
			else:
				print("No encuntro nada, elimino el teclado")
				markup = types.ReplyKeyboardRemove(selective=False)
				bot.send_message(chat_id, "CANCELAR", reply_markup=markup)
		else:
			print("Eliminamos el teclado del Pantalla y borramos la tabla de la BBDD")
			eliminar_usuario_BBDD(chat_id) #Eliminamos el usuario de la BBDD
			markup = types.ReplyKeyboardRemove(selective=False)
			bot.send_message(chat_id, "CANCELAR", reply_markup=markup)


	else:
		print("El usuario '{}' no está en la BBDD".format(chat_id));

		if(message.text.find("shodan")!=-1):
			bi = Biblioteca() #Libreria con funciones propias.
			diccionario = bi.argumentos_validos(message.text)
			if type(diccionario) is not dict:
				cadena=""
				if(diccionario != False):
					cadena+="<b>Error: </b>"+diccionario+"\n\n<b>Ayuda de uso:</b>\n\n"
				cadena+="<b>SHODAN: </b>Shodan es un motor de búsqueda que le permite al usuario encontrar iguales o diferentes tipos específicos de equipos (routers, servidores, etc.) conectados a Internet a través de una variedad de filtros.\n"
				cadena+="\n<b>Ejemplos de uso:</b>\n\n<code>shodan 'búsqueda' 'número de búsquedas'</code>\n\n<code>shodan apache</code>\n<code>shodan apache 5</code>\n"
				cadena+="<code>shodan apache 20</code>.\n\nNota: <b>20</b> es el número máximo de busquedas"
				bot.send_message(chat_id,cadena,parse_mode="HTML")
			else:
				print("Es un diccionario")

				res=""
				if('n' in diccionario):
					res = i.buscar(diccionario["busqueda"],diccionario["n"])
				else:
					res = i.buscar(diccionario["busqueda"])

				resultados = i.nlimit

				if(res==True):
					array_tl = i.datos_telegram()
					#print("token ip: ",i.obtener_token_array_ip())
					guardar_usuario_BBDD(i.obtener_token_array_ip(),message.text,chat_id)
					print("Guardamos usuario({})en la BBDD".format(chat_id))

					markup = crear_teclado_tl(resultados) #creamos el teclado del telegram

					for datos_tl in array_tl:
						bot.send_message(chat_id,datos_tl,parse_mode="HTML")

					#print("Diccionario_IP:",i.diccionario_ip)
					#diccionario_shodan = i.diccionario_ip
					bot.send_message(chat_id,"<b>Elige una opción (1/"+str(resultados)+"): </b>",parse_mode="HTML",reply_markup=markup)

				elif(res==False):
						bot.send_message(chat_id,"No hay ningún resultado con la buscada: <b>"+str(diccionario["busqueda"]+"</b>"),parse_mode="HTML")
				else:
					bot.send_message(chat_id,res,parse_mode="HTML")

		elif message.text == "/autor":
			texto = "<b>Autor:</b> Rubén Gonz. Juan\n"
			texto+= "<b>Github:</b> https://github.com/rubenleon"
			bot.send_message(chat_id, texto,parse_mode="HTML")

		elif message.text == "cancelar":
			markup = types.ReplyKeyboardRemove(selective=False)
			bot.send_message(chat_id, "CANCELAR", reply_markup=markup)


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

def inicializar_bot():
	try:
		bot.polling(True,False,True)
	except requests.exceptions.ReadTimeout:
		print("Timeout occurred")
		time.sleep(2)
		print("Pausa de 2 segundos")
		inicializar_bot()
	except requests.exceptions.ConnectionError:
		print("Error en la conexión")
		time.sleep(2)
		print("Pausa de 2 segundos")
		inicializar_bot()
		#print(except)

inicializar_bot()
