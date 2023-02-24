import sqlite3
from itemadapter import ItemAdapter


class OptlistPipeline:
    def __init__(self):

        with sqlite3.connect('/home/ubuntu/novikn552ta/novikn552ta.sqlite3') as self.con:
            self.cur = self.con.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS links
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                url TEXT
            );""")
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS orders
            (   
                order_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                cardname TEXT,
                category TEXT,
                region TEXT,
                description TEXT
            );""")

        self.con.commit()

    def process_item(self, item, spider):

        if (self.cur.execute(f"SELECT url FROM links WHERE url == ?", (item['url'],)).fetchone()) is None:

            self.cur.execute("INSERT INTO links (url) VALUES (?);", (item['url'],) )

            self.cur.execute("INSERT INTO orders (cardname, category, description, region) VALUES (?, ?, ?, ?);",
            (
                str(item['cardname']),
                str(item['category']),
                str(item['description']),
                str(item['region'])
            ))
            
        self.con.commit()
        return item
