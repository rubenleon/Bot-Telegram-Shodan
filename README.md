# Bot de Telegram de Hacking
> El bot de Telegram incluye herramientas como Shodan, DNS, Whois.

## Creación del Bot

Lo primero que tenemos que hacer es buscar al **@botFather** en el Telegram

![/newbot](img/Telegram-1.jpg)

Pulsamos la opción de */newbot*

![/newbot](/img/Telegram-2.jpg)

Rellenamos la información que nos pide **@botFather** y nos dará la dirección HTTP de nuestro BOT.

## Obtención de la Api de Shodan

Nos vamos a la web oficial de https://www.shodan.io/, nos tenemos que logear y pulsar en el botón **SHOW API KEY**

## Instalación

**Linux** (Ubuntu - Debian):

```sh
pip3 install pyTelegramBotAPI
```

```sh
pip3 install shodan
```

**Linux** (Arch Linux - Antergos):

```sh
pip install pyTelegramBotAPI
```

```sh
pip install shodan
```

## Documentación del Bot

Tenemos que añadir la api de telegram y de shodan en los ficheros:
*shodan-key.txt*
*telegram-key.txt*

Después ejecutamos el archivo de **inicio.py**
