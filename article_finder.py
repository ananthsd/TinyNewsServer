import requests
import json

import psycopg2
from datetime import datetime

def locally_store(categories):

    for category in categories:
        endpoint = "https://api.newscatcherapi.com/v2/search?q="+category+"&page_size=100"
        f = open("newscatcher_api_key.json").read()
        f = json.loads(f)
        headers = {"x-api-key":f['api-key']}
        r = requests.get(endpoint, headers=headers)
        print(r)
        print(r.json())
        f = open(category+".json", "a")
        f.write(json.dumps(r.json()))
        f.close()

def db_get_category_mapping(connection):
    category_cursor = connection.cursor()
    category_cursor.execute("SELECT * FROM Category;")
    categories = category_cursor.fetchall()
    # print(categories)
    mapping = dict()
    for category in categories:
        mapping[category[1].lower()] = category[0]
    category_cursor.close()
    return mapping
def db_store_from_local(categories):
    f = open("postgres_info.json").read()
    f = json.loads(f)
    conn = psycopg2.connect(
    host = f['host'],
    port = f['port'],
    database = f['database'],
    user = f['user'],
    password = f['password'])
    cur = conn.cursor()
    category_mapping = db_get_category_mapping(conn)
    # print(category_mapping)
    for category in categories:
        f = open(category+".json", "r")
        data = json.loads(f.read())
        articles = data['articles']
        for article in articles:
            title = article['title']
            url = article['link']
            picture = article['media']
            text = article['summary']
            time = datetime.strptime(article['published_date'], '%Y-%m-%d %H:%M:%S')
            article_category = category_mapping[category.lower()]
            clean_url = article['clean_url']
            query = """INSERT INTO Article (article_title, article_url, article_picture, article_text, article_time, primary_category, clean_url, categories)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
            print(title)
            cur.execute(query,
            (title, url, picture, text, time, article_category, clean_url, None))
        conn.commit()
    
    cur.close()
    conn.close()


# locally_store(['sports, gaming','Food'])
db_store_from_local(["Sports","Gaming","Food"])
# db_store_from_local(["Food"])
