from flask import Flask, jsonify, request
from main import *
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
app.secret_key = "__privatekey__"
CORS(app)


def __init__(self):
    con = sqlite3.connect('mydb.db')
    c = con.cursor()
    c.execute("CREATE  TABLE user(username text, password text)")
    con.commit()


@app.route("/", methods=['POST'])
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/register', methods=['POST'])
def UserRegister():
    return "<p>Hello, World!</p>"


@app.route('/login', methods=['POST'])
def UserLogin():
    return "<p>Hello, World!</p>"


@app.route('/TF-IDFsearch', methods=['POST'])
def TF_IDFSearch():
    return jsonify(TFIDF(request.json['query']))


if __name__ == '__main__':
    app.run()
