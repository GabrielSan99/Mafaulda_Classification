# https://unicode.org/emoji/charts/full-emoji-list.html
import paho.mqtt.client as mqtt
from threading import Thread
import telebot
import sqlite3
import time
import os


CHAVE_API = "5425249049:AAEptrZ8R8tGGOYIPVmzcJZHb0kpFfqPJTY"
bot = telebot.TeleBot(CHAVE_API)

MQTT_SERVER = "localhost"
TOPICS = ["Status", "Tachometer", "UnderhangAX_plot", "UnderhangRa_plot_", "UnderhangTa_plot", 
                    "OverhangAx_plot", "OverhangRa_plot", "OverhangTa_plot", "Microphone_plot"]

client = mqtt.Client()

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


def verify_and_create_db():
    #falta criar o timestamp
    
    '''
    http://pythonclub.com.br/gerenciando-banco-dados-sqlite3-python-parte1.html

    sqlite3 database.db '.tables' ---------------------> list all tables
    sqlite3 database.db 'PRAGMA table_info(users)' ----> return content on table
    SELECT * FROM users; ------------------------------> get data

    '''
    tables = []
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(tables)
    except:
        print("error")
        
    if tables == []:
        cursor.execute("""
        CREATE TABLE users (
            chat_id INTEGER NOT NULL PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            notify INTEGER NOT NULL
            );
        """)

        print("Database created!")

    else:
        print("User table already exist!")

def verify_and_save_user(chat_id, first_name, last_name):
    new_user = True
    try:
        cursor.execute("SELECT * FROM users WHERE chat_id = {};" .format(chat_id))

        for line in cursor.fetchall():
            print(line)
            if line[0] == int(chat_id):
                print("User already saved!!")
                new_user = False
    except:
        print("User dont exist")

    if new_user == True:
        cursor.execute("""
        INSERT INTO users (chat_id, first_name, last_name, notify)
        VALUES (?,?,?,?)
        """, (chat_id, first_name, last_name, 0))

        conn.commit()
        print("User was saved!!")
    else:
        pass

@bot.message_handler(commands=["status"])
def status(mensagem):
    client.subscribe(TOPICS[0])
    time.sleep(1)
    bot.send_photo(mensagem.chat.id, photo=open('Status.jpeg', 'rb')) #send image


@bot.message_handler(commands=["graphics"])
def graphics(mensagem):
    #Options
    #UA axial, UA radial, UA tangential, OA axial, OA radial, OA tangential, Microphone
    #Envia antes de tudo a imagem contendo informações do que é cada sensor 
    
    texto = """
    O que você quer? (Clique em uma opção)
    /pizza Pizza
    /hamburguer Hamburguer
    /salada Salada"""
    bot.send_message(mensagem.chat.id, texto)

@bot.message_handler(commands=["notify_start"])
def notify_start(mensagem):
    bot.send_message(mensagem.chat.id, "Saindo o Brabo: em 10min chega ai")

@bot.message_handler(commands=["notify_stop"])
def notify_stop(mensagem):
    bot.send_message(mensagem.chat.id, "Não tem salada não, clique aqui para iniciar: /iniciar")

@bot.message_handler(commands=["contact"])
def contact(mensagem):
    text = """
Send me a message with your feedback!!

Phone: +55 (19) 98719-0863
E-mail: gabriel_j.sanches@hotmail.com
    """
    bot.send_message(mensagem.chat.id, text)


def verificar(mensagem):
    print(mensagem)
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """


Welcome to my TCC!! \U0001F393 \U0001F3EB \U0001F393

Choose an option to continue:
(Click on the item)

----------------------------------------------------------------

/status - Mafaulda status \U0001FA7A	

/graphics - get current device measurement graphics \U0001F4C8
     
/notify_start - all status change will send you a notify \U00002705

/notify_stop - stop status change notifications \U0000274C

/contact - show you my contacts \U0001F4F2

----------------------------------------------------------------

Thanks for use my application!! \U0001F604 \U0001F604"""
    
    chat_id = mensagem.chat.id
    first_name = mensagem.chat.first_name
    last_name = mensagem.chat.last_name

    verify_and_save_user(chat_id, first_name, last_name)
    bot.reply_to(mensagem, texto)

def bot_polling():
    bot.polling()

def print_number():
    i = 1
    while True:
        status = input("Status aplicação: ")
        print(status)    
        time.sleep(1)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # for i in range (len(TOPICS)):
    #     client.subscribe(TOPICS[i])

def on_message(client, userdata, msg):
    # more callbacks, etc
    # Create a file with write byte permission

    f = open(msg.topic + '.jpeg', "wb")
    print(msg.payload)
    f.write(msg.payload)
    print("Image Received")
    f.close()

    

def connect_mqtt():

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_SERVER, 1883, 60)
    client.loop_forever()

if __name__ == "__main__":
    verify_and_create_db()
    t1 = Thread(target=bot.polling)
    t2 = Thread(target=connect_mqtt)

    t1.start()
    t2.start()
    

