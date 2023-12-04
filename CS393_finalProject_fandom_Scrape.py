from bs4 import BeautifulSoup
from mysql.connector import connect
from os import path
from requests import get

USERNAME = 'root'
PASSWORD = 'Promethean880x!'

# Connect to the database
cnx = connect(user=USERNAME, password=PASSWORD, database=____________)
cursor = cnx.cursor()

# URL to scrape
url = 'https://fastandfurious.fandom.com/wiki/Category:Cars'
response = get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# SQL queries
INSERT_CAR = '''INSERT INTO Cars (
                    Title, Year, Make, Model
                ) VALUES (%(title)s, %(year)s, %(make)s, %(model)s)
                ON DUPLICATE KEY UPDATE Title=VALUES(Title), Year=VALUES(Year),
                Make=VALUES(Make), Model=VALUES(Model);'''

# Extract car information
for li in soup.find_all('li', class_='category-page__member'):
    title = li.find('a').text.strip()
    year_make_model = title.split()

    if len(year_make_model) >= 3:
        year = year_make_model[0]
        make = year_make_model[1]
        model = ' '.join(year_make_model[2:])

        # Prepare data for the SQL query
        car_data = {'title': title, 'year': year, 'make': make, 'model': model}

        # Execute the SQL query
        cursor.execute(INSERT_CAR, car_data)

# Commit changes and close the database connection
cnx.commit()
cnx.close()
