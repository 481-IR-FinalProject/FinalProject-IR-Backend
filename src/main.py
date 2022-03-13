import jwt
import hashlib
import sqlite3
from symspellpy import SymSpell
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

sym_spell = SymSpell()
con = sqlite3.connect('database/mydb.db', check_same_thread=False)
c = con.cursor()


def getAllData(page):
    data = []
    statement = f"SELECT * FROM food WHERE id BETWEEN 1 + {(page - 1) * 10} AND 10 * {page}"
    dbExecute = c.execute(statement).fetchall()
    index = 0
    statement2 = f"SELECT title FROM food WHERE id BETWEEN 1  AND 10 "
    rows = c.execute(statement2).fetchall()
    for _ in rows:
        try:
            data.append({
                "id": dbExecute[index][0],
                "title": dbExecute[index][1],
                "ingredient": dbExecute[index][2],
                "instruction": dbExecute[index][3],
                "image": dbExecute[index][4],
            })
        except:
            pass
        index += 1
    countFood = f"SELECT COUNT(title) FROM food"

    return [c.execute(countFood).fetchone(), data]


def getFoodSpecificData(id):
    data = []
    statement = f"SELECT * FROM food WHERE id = {id}"
    c.execute(statement)
    dbExecute = c.fetchone()
    data.append({
        "id": dbExecute[0],
        "title": dbExecute[1],
        "ingredient": dbExecute[2],
        "instruction": dbExecute[3],
        "image": dbExecute[4],
    })
    return data[0]


def login(username_in, password_in):
    username = username_in
    password = hashlib.md5(password_in.encode()).hexdigest()
    statement = f"SELECT * from [user] WHERE username = '{username}' AND password='{password}';"
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
    if username_in != "" and password_in != "":
        username = username_in
        password = hashlib.md5(password_in.encode()).hexdigest()
        statement = f"SELECT * from [user] WHERE username = '{username}' AND password='{password}';"
        c.execute(statement)
        data = c.fetchone()
        if data:
            return "<p>Error</p>"
        else:
            if not data:
                c.execute("INSERT INTO [user] (username, password) VALUES (?,?) ", (username, password))
                con.commit()
            return "Register successfully!!!"


def removeFavoriteFoodFromUser(user_id, food_id):
    checkUserExist = c.execute("SELECT id FROM [user]").fetchall()
    checkFoodExist = c.execute("SELECT id FROM food").fetchall()

    if checkUserExist != [] and checkFoodExist != []:
        c.execute("DELETE FROM favorite WHERE user_id = ? AND food_id = ?", (user_id, food_id))
        con.commit()
        return "Remove the favorite food successfully"
    else:
        return "Data not found"


def addFavoriteFoodFromUser(user_id, food_id):
    checkUserExist = c.execute("SELECT id FROM [user]").fetchall()
    checkFoodExist = c.execute("SELECT id FROM food").fetchall()

    if checkUserExist != [] and checkFoodExist != []:
        c.execute("INSERT INTO favorite(user_id, food_id) VALUES (?, ?)",
                  (user_id, food_id))
        con.commit()
        return "Add the favorite food successfully"
    else:
        return "Data not found"


def TFIDF(user_id, readInput, choice, page):
    global choose, corpus_path, bagWord, correctSentence
    dataTFIDF = []
    dataLength = []
    suggestCorrect = readInput
    vectorizer = TfidfVectorizer(ngram_range=(1, 3))
    if choice == "Title":
        choose = c.execute("SELECT title FROM food").fetchall()
        corpus_path = "../src/resources/bagOfWordTitle.txt"
    elif choice == "Ingredient":
        choose = c.execute("SELECT ingredient FROM food").fetchall()
        corpus_path = "../src/resources/bagOfWordIngredient.txt"
    elif choice == "Favorite":
        statement = f"SELECT food_id from favorite WHERE user_id = '{user_id}'"
        c.execute(statement)
        favorite = c.fetchall()
        COLUMN = 0
        column = [elt[COLUMN] for elt in favorite]
        statement2 = f"SELECT title FROM food WHERE id IN ({','.join(['?'] * len(column))})"
        choose = c.execute(statement2, column).fetchall()
        corpus_path = "../src/resources/bagOfWordTitle.txt"
    rows = choose
    COLUMN = 0
    column = [elt[COLUMN] for elt in rows]
    sym_spell.create_dictionary(corpus_path, encoding="utf-8")
    correctSentence = sym_spell.word_segmentation(readInput)
    if not column:
        if suggestCorrect == correctSentence.corrected_string:
            suggestCorrect = ""
        elif suggestCorrect != correctSentence.corrected_string:
            suggestCorrect = correctSentence.corrected_string
        return [len(dataLength), suggestCorrect, dataTFIDF]
    else:
        bagWord = vectorizer.fit_transform(column)
        query_vec = vectorizer.transform([correctSentence.corrected_string])
        results = cosine_similarity(bagWord, query_vec).reshape((-1,))
        index = 1
        index2 = 1
        if choice == "Favorite":
            statement = f"SELECT food_id from favorite WHERE user_id = '{user_id}'"
            c.execute(statement)
            favorite = c.fetchall()
            COLUMN = 0
            column = [elt[COLUMN] for elt in favorite]
            statement2 = f"SELECT id, title, ingredient, instruction, image FROM food WHERE id IN ({','.join(['?'] * len(column))})"
            dbExecute = c.execute(statement2, column).fetchall()
        else:
            dbExecute = c.execute("SELECT id, title, ingredient, instruction, image FROM food").fetchall()
        for i in results.argsort()[:][::-1]:
            if results[i] > 0.1:
                dataLength.append({
                    "id": dbExecute[i][0],
                })
                index += 1
        for i in results.argsort()[-10 * page:][9::-1]:
            if results[i] > 0.1:
                dataTFIDF.append({
                    "id": dbExecute[i][0],
                    "title": dbExecute[i][1],
                    "ingredient": dbExecute[i][2],
                    "instruction": dbExecute[i][3],
                    "image": dbExecute[i][4],
                    "score": results[i]
                })
                index2 += 1
        if suggestCorrect == correctSentence.corrected_string:
            suggestCorrect = ""
        elif suggestCorrect != correctSentence.corrected_string:
            suggestCorrect = correctSentence.corrected_string
    return [len(dataLength), suggestCorrect, dataTFIDF]
