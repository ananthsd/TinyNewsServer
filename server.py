from flask import Flask, flash, request, redirect, jsonify
import json

import psycopg2
import article_finder

app = Flask(__name__)
f = open("postgres_info.json").read()
f = json.loads(f)
conn = psycopg2.connect(
    host = f['host'],
    port = f['port'],
    database = f['database'],
    user = f['user'],
    password = f['password'])
category_mapping = article_finder.db_get_category_mapping(conn)

@app.route('/', methods=['GET'])
def helloWorld():
    return "Hello World"

    

@app.route('/articles/<category>', methods=['GET'])
def getArticles(category):
    # print(category_mapping)
    if not (category.lower() in category_mapping):
        return 'Bad category', 400
    
    limit = request.args.get('limit')
    if limit == None:
        limit = 50
    limit = int(limit)
    if limit > 1000:
        limit = 1000
    
    
    cur = conn.cursor()
    query = """SELECT * FROM Article WHERE primary_category = %s ORDER BY article_time DESC LIMIT %s;"""
    # print(category_mapping[category.lower()])
    cur.execute(query,(category_mapping[category.lower()],limit))
    
    
    data = cur.fetchmany(limit)

    # print(data)

    articles = []
    for article in data:
        articles.append({
            "article_title":article[0], "article_url":article[1], "article_picture":article[2], "article_text":article[3], "article_time":article[4],
                 "primary_category":article[5], "clean_url":article[6], "categories":article[7]
        })
    
    jsonOut = json.dumps(articles, indent=4, sort_keys=True, default=str)
    # print(jsonOut)

    return jsonOut


@app.route('/articles/all', methods=['GET'])
def getAllArticles():
    
    
    limit = request.args.get('limit')
    if limit == None:
        limit = 50
    limit = int(limit)
    if limit > 1000:
        limit = 1000
    
    
    cur = conn.cursor()
    query = """SELECT * FROM article ORDER BY article_time DESC LIMIT %s;"""
    
    cur.execute(query,(limit,))
    
    data = cur.fetchmany(limit)

    # print(data)

    articles = []
    for article in data:
        articles.append({
            "article_title":article[0], "article_url":article[1], "article_picture":article[2], "article_text":article[3], "article_time":article[4],
                 "primary_category":article[5], "clean_url":article[6], "categories":article[7]
        })
    
    jsonOut = json.dumps(articles, indent=4, sort_keys=True, default=str)
    # print(jsonOut)

    return jsonOut
