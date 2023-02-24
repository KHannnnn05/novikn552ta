import os
import sqlite3
import requests
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

with sqlite3.connect('/home/ubuntu/novikn552ta/novikn552ta.sqlite3') as con:
    cur = con.cursor()
token = os.environ.get('TOKEN')
channel_id = os.environ.get('DEV_CHANNEL_ID')

def main():
    for msg in cur.execute("SELECT * FROM orders").fetchall():
        teg = msg[2].replace('.', '').replace(',', '').split()
        if msg[3] != "None":
            message = f'#{"_".join(teg)}\nID -> {msg[0]}\n\n<b>{msg[1]}</b>\n\n{msg[4]}\n\nРегион -> {msg[3]}'
            cur.execute("DELETE FROM orders WHERE order_id == ?", (msg[0], ))
            con.commit()
        else:
            message = f'#{"_".join(teg)}\nID -> {msg[0]}\n\n<b>{msg[1]}</b>\n\n{msg[4]}'
            requests.get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={channel_id}&text={message}&parse_mode=HTML')
            cur.execute("DELETE FROM orders WHERE order_id == ?", (msg[0], ))
            con.commit()
        data = {
            'chat_id': channel_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        requests.get(f'https://api.telegram.org/bot{token}/sendMessage', data)

if (__name__ == "__main__"):
    if cur.execute("SELECT * FROM orders").fetchall() is not None:
        main()
    else:
        pass
