# https://unicode.org/emoji/charts/full-emoji-list.html
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from threading import Thread
from sqlalchemy import null
import telebot
import sqlite3
import pandas as pd
import time
import os


CHAVE_API = "5425249049:AAEptrZ8R8tGGOYIPVmzcJZHb0kpFfqPJTY"
bot = telebot.TeleBot(CHAVE_API)

MQTT_SERVER = "test.mosquitto.org"
TOPICS = ["Status", "Change_status", "Tachometer", "UnderhangAX_plot", "UnderhangRa_plot_", "UnderhangTa_plot", 
                                    "OverhangAx_plot", "OverhangRa_plot", "OverhangTa_plot", "Microphone_plot"]


client = mqtt.Client()

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

possibilities = pd.read_csv("possibilities.csv", index_col=None)
possibilities = possibilities.values.tolist()

response = "Waiting to connect..."
is_image = False
change_notify = False
status_set = False

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
            last_name TEXT,
            notify INTEGER NOT NULL
            );
        """)

        print("Database created!")

    else:
        print("User table already exist!")


def send_user_notify(reponses):
    global status_set
    try:
        if status_set == True:
            cursor.execute("SELECT * FROM users;")

            for user in cursor.fetchall():
                print(user)
                if user[3] == 1:
                    bot.send_message(user[0], response)
                    
            status_set = False
        else:
            pass
    except:
        print("Error into send_user_notify")

    

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
    global is_image, response
    is_image = False

    try:
        cursor.execute("SELECT * FROM users WHERE chat_id = {};" .format(mensagem.chat.id))
        user = cursor.fetchall()
    except:
        print("Falhou")

    if user[0][3] == 0:
        client.subscribe(TOPICS[0])
        time.sleep(1)

        bot.send_message(mensagem.chat.id, response)
        client.unsubscribe(TOPICS[0])
    else:
        client.unsubscribe(TOPICS[0])
        time.sleep(1)
        client.unsubscribe(TOPICS[0])
        bot.send_message(mensagem.chat.id, response)
        


@bot.message_handler(commands=["graphics"])
def graphics(mensagem):
    
    texto = """
Choose a device measurement graphic:
    
----------------------------------------------------------------

/tachometer - Tachometer graphic


/ua_axial - Underhang Accelerometer axial graphic

/ua_radial - Underhang Accelerometer radial graphic

/ua_tangential - Underhang Accelerometer axial graphic


/oa_axial - Overhang Accelerometer axial graphic

/oa_radial - Overhang Accelerometer radial graphic

/oa_tangential - Overhang Accelerometer axial graphic


/microphone - Microphone graphic
"""
    bot.send_message(mensagem.chat.id, texto)

@bot.message_handler(commands=["tachometer"])
def plot_tachometer(mensagem):
    global is_image, responses
    is_image = True

    client.subscribe(TOPICS[2])
    time.sleep(1)
    bot.send_photo(mensagem.chat.id, photo=open("images/" + TOPICS[2] + ".jpeg" , 'rb'))
    client.unsubscribe(TOPICS[2])
    is_image = False

@bot.message_handler(commands=["ua_axial"])
def plot_ua_axial(mensagem):
    global is_image, responses
    is_image = True

    client.subscribe(TOPICS[3])
    time.sleep(1)
    bot.send_photo(mensagem.chat.id, photo=open("images/" + TOPICS[3] + ".jpeg" , 'rb'))
    client.unsubscribe(TOPICS[3])
    is_image = False

@bot.message_handler(commands=["ua_radial"])
def plot_ua_radial(mensagem):
    global is_image, responses
    is_image = True

    client.subscribe(TOPICS[4])
    time.sleep(1)
    bot.send_photo(mensagem.chat.id, photo=open("images/" + TOPICS[4] + ".jpeg" , 'rb'))
    client.unsubscribe(TOPICS[4])
    is_image = False

@bot.message_handler(commands=["ua_tangential"])
def plot_ua_tangential(mensagem):
    global is_image, responses
    is_image = True

    client.subscribe(TOPICS[5])
    time.sleep(1)
    bot.send_photo(mensagem.chat.id, photo=open("images/" + TOPICS[5] + ".jpeg" , 'rb'))
    client.unsubscribe(TOPICS[5])
    is_image = False

@bot.message_handler(commands=["oa_axial"])
def plot_oa_axial(mensagem):
    global is_image, responses
    is_image = True

    client.subscribe(TOPICS[6])
    time.sleep(1)
    bot.send_photo(mensagem.chat.id, photo=open("images/" + TOPICS[6] + ".jpeg" , 'rb'))
    client.unsubscribe(TOPICS[6])
    is_image = False

@bot.message_handler(commands=["oa_radial"])
def plot_oa_radial(mensagem):
    global is_image, responses
    is_image = True

    client.subscribe(TOPICS[7])
    time.sleep(1)
    bot.send_photo(mensagem.chat.id, photo=open("images/" + TOPICS[7] + ".jpeg" , 'rb'))
    client.unsubscribe(TOPICS[7])
    is_image = False

@bot.message_handler(commands=["oa_tangential"])
def plot_oa_tangential(mensagem):
    global is_image, responses
    is_image = True

    client.subscribe(TOPICS[8])
    time.sleep(1)
    bot.send_photo(mensagem.chat.id, photo=open("images/" + TOPICS[8] + ".jpeg" , 'rb'))
    client.unsubscribe(TOPICS[8])
    is_image = False

@bot.message_handler(commands=["microphone"])
def microphone(mensagem):
    global is_image, responses
    is_image = True

    client.subscribe(TOPICS[9])
    time.sleep(1)
    bot.send_photo(mensagem.chat.id, photo=open("images/" + TOPICS[9] + ".jpeg" , 'rb'))
    client.unsubscribe(TOPICS[9])
    is_image = False


@bot.message_handler(commands=["notify_start"])
def notify_start(mensagem):
    cursor.execute("""
        UPDATE users
        SET notify = 1
        WHERE
        chat_id = {}; """ .format(mensagem.chat.id))

    conn.commit()
    bot.send_message(mensagem.chat.id, "Notify started!")

@bot.message_handler(commands=["notify_stop"])
def notify_stop(mensagem):
    cursor.execute("""
    UPDATE users
    SET notify = 0
    WHERE
    chat_id = {}; """ .format(mensagem.chat.id))

    conn.commit()
    bot.send_message(mensagem.chat.id, "Notify stoped!")

@bot.message_handler(commands=["contact"])
def contact(mensagem):
    text = """
Send me a message with your feedback!!

Phone: +55 (19) 98719-0863
E-mail: gabriel_j.sanches@hotmail.com
    """
    bot.send_message(mensagem.chat.id, text)

@bot.message_handler(commands=["set_status"])
def set_status(mensagem):
    global is_image
    is_image = False
    
    
    text = "This is all possibilities: \n\n" 
    for i in range (len(possibilities)):
        string = str(i) + "-" + possibilities[i][0] + "\n"
        text = text + string

    text = text + "\n\n To set a new status use the following notation: \n\n Set_status {possibilities_index}"
    bot.send_message(mensagem.chat.id, text)


def verify_change_status(mensagem):
    if "Set_status" in mensagem.text:
        return True

@bot.message_handler(func=verify_change_status)
def change_status(mensagem):
    global status_set

    space_index = mensagem.text.find(" ")
    number = int(mensagem.text[space_index+1:])

    publish.single(TOPICS[1], possibilities[number][0], hostname= MQTT_SERVER, retain=True) 
    bot.send_message(mensagem.chat.id, "Status changed to: " + possibilities[number][0])
    status_set = True

def verify(mensagem):
    print(mensagem.text)
    return True

@bot.message_handler(func=verify)
def answer(mensagem):
    global chat_id
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

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TOPICS[0])
    # check_user_notify()

def on_message(client, userdata, msg):
    global is_image, response

    if is_image == False:
        response = str(msg.payload.decode())
        send_user_notify(response)
    else:
        f = open("images/" + msg.topic + '.jpeg', "wb")
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
    

