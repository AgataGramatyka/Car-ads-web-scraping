# Using Beautiful Soup to scrape information from car sale ads

This code was written specifically to obtain data from a leading European used car sales website. Done for purely non-commercial purposes, the data on car sales was used in a machine learning study.

### The first program (Scrape_car_links.py)

1) creates an SQL database
```
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
```

2) crawls through the website and stores links to each individual ad in the database

```
cur.execute('SELECT id FROM Ads WHERE url is NULL ORDER BY RANDOM() LIMIT 1')
row = cur.fetchone()
if row is not None:
    print("Restarting existing crawl.")


start_time = time()
pagecount = 1
many = 0
while many < 2 :
    url = 'hiddenurl' + str(pagecount) + '.html'
    many += 1
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
```
### The second program (Scrape_car_ads.py)

1) accesses each of the links individually,

```
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
```

2) scrapes html data including car make, model, year of registration, mileage etc.

```
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
```

3) The data is then written into the SQL database
```
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
  ```
