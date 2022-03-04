import hashlib
import sqlite3

import jwt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spellchecker import SpellChecker

try:
    cleanData = pd.read_csv("resources/FoodCleanedData.csv")
except:
    cleanData = pd.read_csv("src/resources/FoodCleanedData.csv")
spellChecker = SpellChecker()


def getAllData(page):
    try:
        con = sqlite3.connect('src/database/mydb.db')
    except:
        con = sqlite3.connect('database/mydb.db')
    c = con.cursor()
    data = []
    dbExcute = c.execute("SELECT * FROM food").fetchall()
    index = 0
    rows = c.execute("SELECT title FROM food").fetchall()
    for _ in rows:
        data.append({
            "id": dbExcute[index][0],
            "title": dbExcute[index][1],
            "ingredient": dbExcute[index][2],
            "instruction": dbExcute[index][3],
            "image": dbExcute[index][4],
        })
        index += 1
    data = [data[i:i + 10] for i in range(0, len(data), 10)]
    page -= 1
    return data[page]


def getFoodSpecificData(id):
    try:
        con = sqlite3.connect('src/database/mydb.db')
    except:
        con = sqlite3.connect('database/mydb.db')
    c = con.cursor()
    data = []
    dbExcute = c.execute("SELECT * FROM food").fetchall()
    index = 0
    rows = c.execute("SELECT title FROM food").fetchall()
    for _ in rows:
        data.append({
            "id": dbExcute[index][0],
            "title": dbExcute[index][1],
            "ingredient": dbExcute[index][2],
            "instruction": dbExcute[index][3],
            "image": dbExcute[index][4],
        })
        index += 1
    id -= 1
    return data[id]


def login(username_in, password_in):
    username = username_in
    password = hashlib.md5(password_in.encode()).hexdigest()
    try:
        con = sqlite3.connect('src/database/mydb.db')
    except:
        con = sqlite3.connect('database/mydb.db')
    c = con.cursor()
    statement = f"SELECT * from user WHERE username = '{username}' AND password='{password}';"
    c.execute(statement)
    data = c.fetchone()
    encoded_jwt = jwt.encode({"id": data[0], "username": data[1]}, "secret", algorithm="HS256")

    result = {
        "token": encoded_jwt,
        "user": {
            "id": data[0],
            "username": data[1]
        }
    }
    return result


def getUserFavoriteFood(user_id):
    try:
        con = sqlite3.connect('src/database/mydb.db')
    except:
        con = sqlite3.connect('database/mydb.db')
    c = con.cursor()

    statement = f"SELECT food_id from favorite WHERE user_id = '{user_id}'"
    c.execute(statement)
    favorite = c.fetchall()
    COLUMN = 0
    column = [elt[COLUMN] for elt in favorite]
    statement2 = f"SELECT * from food WHERE id IN ({','.join(['?'] * len(column))})"
    c.execute(statement2, column)
    food = c.fetchall()
    data = []
    index = 0
    for _ in column:
        data.append({"id": food[index][0],
                     "title": food[index][1],
                     "ingredient": food[index][2],
                     "instruction": food[index][3],
                     "image": food[index][4]})
        index += 1
    return data


def register(username_in, password_in):
    try:
        con = sqlite3.connect('src/database/mydb.db')
    except:
        con = sqlite3.connect('database/mydb.db')
    c = con.cursor()
    if (username_in != "" and password_in != ""):
        username = username_in
        password = hashlib.md5(password_in.encode()).hexdigest()
        statement = f"SELECT * from user WHERE username = '{username}' AND password='{password}';"
        c.execute(statement)
        data = c.fetchone()
        if data:
            return "<p>Error</p>"
        else:
            if not data:
                c.execute("INSERT INTO user (username, password) VALUES (?,?) ", (username, password))
                con.commit()
                con.close()
            return "Register successfully!!!"


def TFIDF(readInput):
    dataTFIDF = []
    spellCorrection = []
    spellCandidate = []
    keepSpell = readInput.split(" ")
    vectorizer = TfidfVectorizer()
    df_all = pd.DataFrame(cleanData, columns=['title', 'ingredient', 'instruction', 'image'])
    bagWord = vectorizer.fit_transform(cleanData['title'])
    index = 0
    for _ in keepSpell:
        spellCorrection.append(spellChecker.correction(keepSpell[index]))
        spellCandidate.append(spellChecker.candidates(keepSpell[index]))
        index += 1

    correctSentence = ' '.join(map(str, spellCorrection))

    query_vec = vectorizer.transform([correctSentence])
    results = cosine_similarity(bagWord, query_vec).reshape((-1,))
    index = 1
    for i in results.argsort()[:][::-1]:
        if results[i] > 0.1:
            dataTFIDF.append({
                "id": index,
                "title": df_all.iloc[i, 0],
                "ingredient": df_all.iloc[i, 1],
                "instruction": df_all.iloc[i, 2],
                "image": df_all.iloc[i, 3],
                "score": results[i]
            })
            index += 1
    print("Correction: ", spellCorrection)
    print("Candidate: ", spellCandidate)
    print("Correct sentence:", correctSentence)
    return dataTFIDF
