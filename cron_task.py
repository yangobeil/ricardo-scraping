from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import ssl
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pymongo import MongoClient
import requests

# load environment variables
load_dotenv()
EMAIL_PASSWORD = os.getenv('SENDER_EMAIL_PASSWORD')
SENDER_EMAIL = os.getenv('SENDER_EMAIL_ADDRESS')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL_ADDRESS')
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

# connect to mongoDB
host = f'mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@recipes-3neas.mongodb.net/Ricardo?retryWrites=true&w=majority'
client = MongoClient(host=host)
db = client.Ricardo
collection = db.recipes
print("Connected to mongoDB")

# setup global variables
PORT = 465  # For SSL
error = None

try:
    # extract number of recipes from website
    main_search_url = "https://www.ricardocuisine.com/recherche/mot-cle//page/1"
    main_page = requests.get(main_search_url)
    main_soup = BeautifulSoup(main_page.content, features="lxml")
    num_recipes = int(main_soup.find('a', {'href': '/recherche/mot-cle//tab/recipe/page/1/facet/'}).find('span').contents[0][1:-1])
    num_pages = num_recipes // 20
    print("Found {} pages of recipes".format(num_pages))

    # load old list of recipes
    old_recipes = collection.find()

    # extract list of recipes on website
    downloaded_recipes = []
    for i in range(num_pages):
        search_url = "https://www.ricardocuisine.com/recherche/mot-cle//page/{}".format(str(i+1))
        page = requests.get(search_url)
        soup = BeautifulSoup(page.content, features="lxml")
        for element in soup.find('div', {'id': 'search-results'}).find_all('a', {'class': 'parent'}):
            recipe_title = element['title']
            recipe_url = "https://www.ricardocuisine.com" + element['href']
            recipe_data = {'url': recipe_url,
                           'title': recipe_title}
            downloaded_recipes.append(recipe_data)
        if i % 25 == 0:
            print(i)
        time.sleep(10)

    print(len(downloaded_recipes))
    old_recipes_titles = [item['title'] for item in old_recipes]
    new_recipes = [item for item in downloaded_recipes if item['title'] not in old_recipes_titles]
    print(len(new_recipes))

    # save new list of recipes
    if len(new_recipes) > 0:
        collection.insert_many(new_recipes)

    print("Found the list of recipes")

except Exception as e:
    new_recipes = []
    error = e
    print("There was an error when searching for recipes: {}".format(error))


def create_email(new_recipes, error):
    if error:
        text = "Il y a eu une erreur avec la recherche: {}".format(error)
        html = "<p>Il y a eu une erreur avec la recherche: {}</p>".format(error)
    elif len(new_recipes) == 0:
        text = "Il n'y a pas de nouvelles recettes"
        html = "<p>Il n'y a pas de nouvelles recettes</p>"
    else:
        text = ""
        html = ""
        for item in new_recipes:
            text = text + item['title'] + "\n\n"
            html = html + "<a href='{}'>{}</a></br></br>".format(item['url'], item['title'])
    return text, html


message = MIMEMultipart("alternative")
message["Subject"] = "Nouvelles recettes de Ricardo"
message["From"] = SENDER_EMAIL
message["To"] = RECEIVER_EMAIL

text, html = create_email(new_recipes, error)

part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")
message.attach(part1)
message.attach(part2)

# Create a secure SSL context
try:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
    print("Email has been sent")
except Exception as e:
    print("There was an error when sending the email: {}".format(e))
