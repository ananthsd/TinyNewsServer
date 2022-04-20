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
            "article_id": article[0], "article_title":article[1], "article_url":article[2], "article_picture":article[3], "article_text":article[4], "article_time":article[5],
                 "primary_category":article[6], "clean_url":article[7], "categories":article[8]
        })
    
    jsonOut = json.dumps(articles, indent=4, sort_keys=True, default=str)
    # print(jsonOut)

    return jsonOut

@app.route('/categories', methods=['GET'])
def getCategories():
    print(category_mapping)
    jsonOut = json.dumps(category_mapping, indent=4, sort_keys=True, default=str)
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
            "article_id": article[0], "article_title":article[1], "article_url":article[2], "article_picture":article[3], "article_text":article[4], "article_time":article[5],
                 "primary_category":article[6], "clean_url":article[7], "categories":article[8]
        })
    
    jsonOut = json.dumps(articles, indent=4, sort_keys=True, default=str)
    # print(jsonOut)

    return jsonOut

@app.route('/articles/preference', methods=['GET'])
def getArticlesByPreference():
    # print(category_mapping)
    categories = request.args.getlist('categories')
    broadcasters = request.args.getlist('broadcasters')
    # print(category_mapping)
    # print(categories)
    # print(broadcasters)
    has_categories = categories != None and categories != []
    has_broadcasters = broadcasters != None and broadcasters != []
    if  (not has_categories) and (not has_broadcasters):
        return 'Missing Argument(s) {categories or broadcasters}', 400
    
    limit = request.args.get('limit')
    if limit == None:
        limit = 50
    limit = int(limit)
    if limit > 1000:
        limit = 1000

    

    if has_categories:
        categories2 = []
        for category in categories:
            categories2.append(category_mapping[category.lower()])
        categories = categories2
        categories = tuple(categories)

    
    if has_broadcasters:    
        broadcasters = tuple(broadcasters)

    cur = conn.cursor()
    if has_categories and has_broadcasters:
        query = """SELECT * FROM Article WHERE primary_category in %s or clean_url in %s ORDER BY article_time DESC LIMIT %s;"""
        cur.execute(query,(categories, broadcasters,limit))
    elif has_categories:
        query = """SELECT * FROM Article WHERE primary_category in %s ORDER BY article_time DESC LIMIT %s;"""
        cur.execute(query,(categories,limit))
    else:
        query = """SELECT * FROM Article WHERE clean_url in %s ORDER BY article_time DESC LIMIT %s;"""
        cur.execute(query,(broadcasters,limit))
    
    
    data = cur.fetchmany(limit)

    # print(data)

    articles = []
    for article in data:
        articles.append({
            "article_id": article[0], "article_title":article[1], "article_url":article[2], "article_picture":article[3], "article_text":article[4], "article_time":article[5],
                 "primary_category":article[6], "clean_url":article[7], "categories":article[8]
        })
    
    jsonOut = json.dumps(articles, indent=4, sort_keys=True, default=str)
    # print(jsonOut)

    return jsonOut
