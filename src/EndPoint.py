from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/TF-IDFsearch', methods=['POST'])
def TF_IDFSearch():
    return jsonify(TFIDF(request.json['query']))

if __name__ == '__main__':
    app.run()