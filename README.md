# Bot de Telegram de Hacking
> El bot de Telegram incluye herramientas como Shodan, DNS, Whois.

## Creación del Bot

Lo primero que tenemos que hacer es buscar al **@botFather** en el Telegram

![/newbot](img/Telegram-1.jpg)

Pulsamos la opción de */newbot*

![/newbot](/img/Telegram-2.jpg)

Rellenamos la información que nos pide **@botFather** y nos dará **TOKEN** de nuestro BOT.

## Añadir Comandos al Bot

> 1. Escribimos el comando **/mybots**.

![/newbot](img/Telegram-3.jpg)

> 2. Editamos el Bot pulsando en el botón **Edit Bot**

![/newbot](img/Telegram-4.jpg)

> 3. Pulsamos en el botón de **Edit Commands** y escribimos la lista de comandos con este formato:

```sh
shodan - busqueda
autor - autor del bot
```

![/newbot](img/Telegram-5.jpg)

## Obtención de la Api de Shodan

Entramos en la web oficial de https://www.shodan.io/ y pulsamos en el botón **SHOW API KEY**

## Instalación

**Linux** (Ubuntu - Debian):

```sh
pip3 install pyTelegramBotAPI
```

```sh
pip3 install shodan
```

```sh
pip3 install sqlite3
```


**Linux** (Arch Linux - Antergos):

```sh
pip install pyTelegramBotAPI
```

```sh
pip install shodan
```

```sh
pip install sqlite3
```

## Documentación del Bot

Tenemos que añadir la clave de shodan y de telegram a los siguientes ficheros:
*shodan-key.txt*
*telegram-key.txt*

## Ejecución del Bot

Ejecutamos el archivo **inicio.py**

**Linux** (Ubuntu - Debian):

```sh
python3 inicio.py
```

**Linux** (Arch Linux - Antergos):

```sh
python inicio.py
```
## Base de Datos

Para visualizar la Base de Datos utilizamos la siguiente aplicación: http://sqlitebrowser.org/

## Video del Bot en Acción

[![Video del Bot](img/video.jpg)](https://www.youtube.com/watch?v=Zpngydf6iwQ)
