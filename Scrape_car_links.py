from requests import get
from bs4 import BeautifulSoup
from time import sleep
from time import time
import sqlite3

conn = sqlite3.connect('cars.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Ads
            (id INTEGER PRIMARY KEY, url TEXT UNIQUE,
            Title TEXT, Price INTEGER, Model TEXT,
            Year TEXT, Mileage INTEGER, Doors TEXT,
            BhpF TEXT, BhpD TEXT, Gearbox TEXT,
            Fueltype TEXT, Regdate DATE, Seats TEXT,
            Colour TEXT, Retrieved INTEGER)''')

cur.execute('SELECT id FROM Ads WHERE url is NULL ORDER BY RANDOM() LIMIT 1')
row = cur.fetchone()
if row is not None:
    print("Restarting existing crawl.")


start_time = time()
pagecount = 1
many = 0
while many < 2 :
    url = 'hiddenurl' + str(pagecount) + '.html'
    many = many + 1
    pagecount = pagecount + 1
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    car_ads = soup.find_all('a', class_='linkAd')
    for ad in car_ads:
        adurl = 'hiddenurl' + ad.get('href', None)
        cur.execute('INSERT OR IGNORE INTO Ads (url) VALUES (?)', (adurl,))
        conn.commit()
    sleep(3)
print(time() - start_time)

cur.close()
