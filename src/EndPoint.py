from flask import Flask, jsonify, request
from main import *
from flask_cors import CORS
import sqlite3
import hashlib
import jwt

app = Flask(__name__)
app.secret_key = "__privatekey__"
CORS(app)

try:
    con = sqlite3.connect('src/database/mydb.db')
except:
    con = sqlite3.connect('database/mydb.db')
c = con.cursor()
try:
    c.execute("CREATE TABLE user(id INTEGER, username text UNIQUE, password text, PRIMARY KEY (id))")
    c.execute(
        "CREATE TABLE food(id INTEGER, title text, ingredient text, instruction text, image text, PRIMARY KEY (id))")
    c.execute(
        "CREATE TABLE favorite(id INTEGER, user_id INTEGER NOT NULL, food_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES user (id),  FOREIGN KEY (food_id) REFERENCES food (id), PRIMARY KEY (id))")
except:
    print("Table already exist")
con.commit()


@app.route("/getAllData/page=<int:page>", methods=['GET'])
def getAll(page=1):
    if page < 1:
        return "Minimum page is 1"
    else:
        try:
            return jsonify(getAllData(page))
        except:
            return "Page is exceed the limit"


@app.route("/getFood/<int:id>", methods=['GET'])
def getFoodByID(id):
    if id < 1:
        return "Minimum page is 1"
    else:
        try:
            return jsonify(getFoodSpecificData(id))
        except:
            return "Page is exceed the limit"


@app.route('/register', methods=['POST'])
def UserRegister():
    try:
        con = sqlite3.connect('src/database/mydb.db')
    except:
        con = sqlite3.connect('database/mydb.db')
    c = con.cursor()
    if (request.json['username'] != "" and request.json['password'] != ""):
        username = request.json['username']
        password = hashlib.md5(request.json['password'].encode()).hexdigest()
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


@app.route('/login', methods=['POST'])
def UserLogin():
    username = request.json['username']
    password = hashlib.md5(request.json['password'].encode()).hexdigest()
    try:
        con = sqlite3.connect('src/database/mydb.db')
    except:
        con = sqlite3.connect('database/mydb.db')
    c = con.cursor()
    statement = f"SELECT * from user WHERE username = '{username}' AND password='{password}';"
    c.execute(statement)
    data = c.fetchone()
    encoded_jwt = jwt.encode({"id": data[0], "username": data[1]}, "secret", algorithm="HS256")
    statement2 = f"SELECT food_id from favorite WHERE user_id = '{data[0]}'"
    c.execute(statement2)
    favorite = c.fetchall()
    result = {
        "token": encoded_jwt,
        "user": {"username": data[1],
                 "favorite": favorite
                 }
    }
    return result


@app.route("/addFavorite", methods=['POST'])
def addToFavorite():
    try:
        con = sqlite3.connect('src/database/mydb.db')
    except:
        con = sqlite3.connect('database/mydb.db')
    c = con.cursor()
    checkUserExist = c.execute("SELECT id FROM user").fetchall()
    checkFoodExist = c.execute("SELECT id FROM food").fetchall()

    if (checkUserExist != [] and checkFoodExist != []):
        c.execute("INSERT INTO favorite(user_id, food_id) VALUES (?, ?)",
                  (request.json['user_id'], request.json['food_id']))
        con.commit()
        con.close()
        return "Add the favorite food successfully"
    else:
        return "Data not found"


@app.route("/removeFavorite", methods=['POST'])
def removeFavorite():
    try:
        con = sqlite3.connect('src/database/mydb.db')
    except:
        con = sqlite3.connect('database/mydb.db')
    c = con.cursor()
    checkUserExist = c.execute("SELECT id FROM user").fetchall()
    checkFoodExist = c.execute("SELECT id FROM food").fetchall()

    if (checkUserExist != [] and checkFoodExist != []):
        c.execute("DELETE FROM favorite WHERE user_id = ? AND food_id = ?",
                  (request.json['user_id'], request.json['food_id']))
        con.commit()
        con.close()
        return "Remove the favorite food successfully"
    else:
        return "Data not found"


@app.route('/TF-IDFsearch', methods=['POST'])
def TF_IDFSearch():
    return jsonify(TFIDF(request.json['query']))


if __name__ == '__main__':
    app.run()
