import requests
import json
import time
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
        time.sleep(1.5)

def locally_store_topics(topics):

    for topic in topics:
        endpoint = "https://api.newscatcherapi.com/v2/latest_headlines?topic="+topic+"&page_size=100&lang=en"
        f = open("newscatcher_api_key.json").read()
        f = json.loads(f)
        headers = {"x-api-key":f['api-key']}
        r = requests.get(endpoint, headers=headers)
        print(r)
        print(r.json())
        f = open(topic+".json", "a")
        f.write(json.dumps(r.json()))
        f.close()
        time.sleep(1.5)

def locally_store_sources(sources):

    for source in sources:
        endpoint = "https://api.newscatcherapi.com/v2/latest_headlines?sources="+source+"&page_size=100&lang=en"
        f = open("newscatcher_api_key.json").read()
        f = json.loads(f)
        headers = {"x-api-key":f['api-key']}
        r = requests.get(endpoint, headers=headers)
        print(r)
        print(r.json())
        f = open(source+".json", "a")
        f.write(json.dumps(r.json()))
        f.close()
        time.sleep(1.5)

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

def db_store_from_local_by_topic(topics):
    f = open("postgres_info.json").read()
    f = json.loads(f)
    conn = psycopg2.connect(
    host = f['host'],
    port = f['port'],
    database = f['database'],
    user = f['user'],
    password = f['password'])
    cur = conn.cursor()
    topic_mapping = {'tech' : 'Technology', 'news' : 'News', 'business' : 'Business',
     'science': 'Science', 'finance': 'Finance', 'food': 'Food', 'politics': 'Politics',
      'economics': 'Economics', 'travel': 'Travel', 'entertainment': 'Economics',
       'music': 'Music', 'sport': 'Sports', 'world': 'World'}
    category_mapping = db_get_category_mapping(conn)
    # print(category_mapping)
    for topic in topics:
        f = open(topic+".json", "r")
        data = json.loads(f.read())
        articles = data['articles']
        for article in articles:
            title = article['title']
            url = article['link']
            picture = article['media']
            text = article['summary']
            if text == None:
                continue
            time = datetime.strptime(article['published_date'], '%Y-%m-%d %H:%M:%S')
            article_category = category_mapping[topic_mapping[topic.lower()].lower()]
            clean_url = article['clean_url']
            query = """INSERT INTO Article (article_title, article_url, article_picture, article_text, article_time, primary_category, clean_url, categories)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
            print(title)
            cur.execute(query,
            (title, url, picture, text, time, article_category, clean_url, None))
        conn.commit()
    
    cur.close()
    conn.close()


def db_store_from_local_by_source(sources):
    f = open("postgres_info.json").read()
    f = json.loads(f)
    conn = psycopg2.connect(
    host = f['host'],
    port = f['port'],
    database = f['database'],
    user = f['user'],
    password = f['password'])
    cur = conn.cursor()
    topic_mapping = {'tech' : 'Technology', 'news' : 'News', 'business' : 'Business',
     'science': 'Science', 'finance': 'Finance', 'food': 'Food', 'politics': 'Politics',
      'economics': 'Economics', 'travel': 'Travel', 'entertainment': 'Economics',
       'music': 'Music', 'sport': 'Sports', 'world': 'World', 'gaming': 'Gaming','beauty': 'Beauty','energy': 'Energy'}
    category_mapping = db_get_category_mapping(conn)
    # print(category_mapping)
    for source in sources:
        f = open(source+".json", "r")
        data = json.loads(f.read())
        articles = data['articles']
        for article in articles:
            title = article['title']
            url = article['link']
            picture = article['media']
            text = article['summary']
            if text == None:
                continue
            time = datetime.strptime(article['published_date'], '%Y-%m-%d %H:%M:%S')
            article_category = category_mapping[topic_mapping[article['topic']].lower()]
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
# locally_store([
# 'Health',
# 'Lifestyles',
# 'Politics',
# 'Science'])
# db_store_from_local(["Sports","Gaming","Food"])
# db_store_from_local([
# 'Economics',
# 'Entertainment',
# 'Health',
# 'Lifestyles',
# 'Politics',
# 'Science',])

# locally_store_topics(['tech', 'business', 'science', 'finance', 'food', 'politics', 'economics', 'travel', 'entertainment', 'music', 'sport', 'world'])
# db_store_from_local_by_topic(['tech' , 'business', 'science', 'finance', 'food', 'politics', 'economics', 'travel', 'entertainment', 'music', 'sport', 'world'])

# locally_store_sources(["latimes.com","cnn.com","foxnews.com","theatlantic.com","politico.com","9to5mac.com","abc.com","theguardian.com","yahoo.com"])
# db_store_from_local_by_source(["latimes.com","cnn.com","foxnews.com","theatlantic.com","politico.com","9to5mac.com","abc.com","theguardian.com","yahoo.com"])