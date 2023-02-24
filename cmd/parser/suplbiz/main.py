import sqlite3
import datetime
import requests
from urllib.parse import quote

base_url = 'https://supl.biz'
auth_url = 'https://supl.biz/api/monolith/auth/'
query_url = 'https://supl.biz/api/monolith/orders/elsearch/?query=&rubrics={category_id}&statuses=completed,published&hide_viewed=false&is_international=false&gradation=0,1,2,3&filter_by_supply_city=false&show_blocked_users=false&size=25&exact=true&actualized_at_lt={date}'
data = {
    'email': 'ashamil435@gmail.com',
    'password': 'Abdulaev005'
}

headers = {
    'accept': '*/*',
    'user-agent': 'parser ashm.tech'
}

category = requests.get('https://supl.biz/api/monolith/rubrics/tree/ru/').json()

with sqlite3.connect('/home/ubuntu/novikn552ta/novikn552ta.sqlite3') as con:
    cur = con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS links
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        url TEXT
    );""")
cur.execute("""
CREATE TABLE IF NOT EXISTS orders
    (   
        order_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        cardname TEXT,
        category TEXT,
        region TEXT,
        description TEXT
    );""")

con.commit()

s = requests.Session()
s.headers.update(headers)
s.post(auth_url, data)

for i in (category): 
    data = s.get(url=query_url.format(
            date=quote(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f+03:00')),
            category_id=i['id'])).json()['hits']
    for info in data:
        url = base_url + info['url']
        if (cur.execute(f"SELECT url FROM links WHERE url == ?", (url,))).fetchone() is None:
            cur.execute("INSERT INTO links (url) VALUES (?);", (url,) )
            cur.execute("INSERT INTO orders (cardname, category, description, region) VALUES (?, ?, ?, ?);",
            (   
                str(info['meta_title']),
                str(i['title']),
                str(info['description']),
                str(info['supply_city']['title'])
            ))

con.commit()