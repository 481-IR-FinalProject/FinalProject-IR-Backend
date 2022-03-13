from flask import Flask, jsonify, request
from main import *
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

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
        return jsonify(getAllData(page))


@app.route("/getFood/<int:id>", methods=['GET'])
def getFoodByID(id):
    if id < 1:
        return "Minimum page is 1"
    else:
        return jsonify(getFoodSpecificData(id))


@app.route('/register', methods=['POST'])
def UserRegister():
    return register(request.json['username'], request.json['password'])


@app.route('/login', methods=['POST'])
def UserLogin():
    return login(request.json['username'], request.json['password'])


@app.route("/addFavorite", methods=['POST'])
def addToFavorite():
    return jsonify(addFavoriteFoodFromUser(request.json['user_id'], request.json['food_id']))


@app.route("/removeFavorite", methods=['POST'])
def removeFavorite():
    return jsonify(removeFavoriteFoodFromUser(request.json['user_id'], request.json['food_id']))


@app.route("/getFavorite", methods=['POST'])
def getFavorite():
    return jsonify(getUserFavoriteFood(request.json['user_id']))


@app.route('/TF-IDFsearch/page=<int:page>', methods=['POST'])
def TF_IDFSearch(page=1):
    if page < 1:
        return "Minimum page is 1"
    else:
        return jsonify(TFIDF(request.json['user_id'], request.json['query'], request.json['type'], page))


if __name__ == '__main__':
    app.run()
