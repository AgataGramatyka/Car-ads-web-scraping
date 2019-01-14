# Using Beautiful Soup to scrape information from car sale ads

This code was written specifically to obtain data from a leading European used car sales website. Done for purely non-commercial purposes, the data on car sales was used in a machine learning study.

The first program (Scrape_car_links.py):
1) creates an SQL database,
2) crawls through the website
3) and stores links to each individual ad in the database.

The second program (Scrape_car_ads.py): 
1) accesses each of the links individually,
2) scrapes html data including car make, model, year of registration, mileage etc.
3) The data is then written into the SQL database.
