from sqlalchemy import null
import telebot
import sqlite3
import time
import os

new_user = True

conn = sqlite3.connect('database.db')
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
            last_name TEXT NOT NULL
            );
        """)

        print("Database created!")

    else:
        print("User table already exist!")


def input_insert_data():

    c_id = input('Chat id: ')
    f_name = input('First name: ')
    l_name = input('Last name: ')

    cursor.execute("""
    INSERT INTO users (chat_id, first_name, last_name)
    VALUES (?,?,?)
    """, (c_id, f_name, l_name))

    conn.commit()



def verify_and_save_user(chat_id):
    new_user = get_data(chat_id)
    if new_user == True:
        input_insert_data()
    else:
        pass

def get_data(chat_id):

    try:
        cursor.execute("SELECT * FROM users WHERE chat_id = {};" .format(chat_id))

        for line in cursor.fetchall():
            print(line)
            if line[0] == int(chat_id):
                print("User already saved!!")
                return False
    except:
        print("User dont exist")
        return True

            


if __name__ == "__main__":
    
    verify_and_create_db()
    verify_and_save_user(12345)
    #input_insert_data()
    #get_data(1234)
    conn.close()
    
