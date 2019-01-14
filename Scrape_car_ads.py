from requests import get
from bs4 import BeautifulSoup
from time import sleep
from time import time
from datetime import date
import sqlite3

conn = sqlite3.connect('cars.sqlite')
cur = conn.cursor()

start_time = time()
many = 0 #counter
crawl_attempts = 50 #maximum number of ads accessed in one round of scraping

while many < crawl_attempts :
    many += 1
    cur.execute('SELECT url FROM Ads WHERE Retrieved IS NULL LIMIT 1')
    try:
        URL = cur.fetchone()[0]
        print(URL)
    except:
        continue
    response = get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    header = soup('div', class_='mainInfos')
    if len(header) > 0 :
        try:
            infgen = soup('div', class_='box boxOptions infosGen')
            for h in header:
                title = str(h.h1.div.text.strip())
                price = int(h.strong.text.strip().replace('\xa0€','').replace(' ',''))

            for i in infgen:
                model = i.h3.span.text.strip()

            ul = soup.find('ul', {'class': 'infoGeneraleTxt column2'})
            children = ul.findChildren('li', recursive=False)
            count = 10
            desc = list()
            for child in children:
                desc.append(child.span.text.replace('\xa0',''))
                print(desc)
                count = count - 1
                if count == 0: break
                year = desc[0]
                mileage = int(desc[1].replace('km','').replace(' ',''))
                doors = desc[2].strip()
                bhpf = desc[3].strip()
                bhpd = desc[4].strip()
                gearbox = desc[5].strip()
                fueltype = desc[6].strip()
                regdate = desc[7].strip()
                seats = desc[8].strip()
                colour = desc[9].strip()

            cur.execute('''UPDATE Ads SET Title=?, Price=?, Model=?, Year=?, Mileage=?,
            Doors=?, BhpF=?, BhpD=?, Gearbox=?, Fueltype=?, Regdate=?, Seats=?, Colour=?, Retrieved=1
            WHERE url = ?''', (title, price, model, year, mileage, doors, bhpf, bhpd, gearbox, fueltype, regdate, seats, colour, URL))
            conn.commit()
        except:
            cur.execute('UPDATE Ads SET Retrieved=-1 WHERE url=?', (URL,))
            print('row to examine')
            conn.commit()
    else:
        cur.execute('DELETE FROM Ads WHERE url=?', (URL,))
        print('row deleted')
        conn.commit()

    sleep(2)
print(time() - start_time)
cur.close()
