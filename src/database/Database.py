import csv
import sqlite3

from sklearn.feature_extraction.text import TfidfVectorizer
from symspellpy import SymSpell

sym_spell = SymSpell()
con = sqlite3.connect("mydb.db")
cur = con.cursor()


def addFoodIntoDatabase():
    a_file = open("../resources/FoodCleanedData.csv", encoding='utf-8')
    rows = csv.reader(a_file)
    next(rows)
    cur.executemany("INSERT INTO food(title, ingredient, instruction, image) VALUES (?, ?, ?, ?)", rows)
    con.commit()
    con.close()


def dropFood():
    cur.execute("DELETE FROM food")
    con.commit()


def dropFavorite():
    cur.execute("DELETE FROM favorite")
    con.commit()
    con.close()


def dropUser():
    cur.execute("DELETE FROM [user]")
    con.commit()
    con.close()


def bagOfWordToTxT(choice):
    global choose
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    if choice == "Title":
        choose = cur.execute("SELECT title FROM food").fetchall()
    elif choice == "Ingredient":
        choose = cur.execute("SELECT ingredient FROM food").fetchall()
    rows = choose
    COLUMN = 0
    column = [elt[COLUMN] for elt in rows]
    vectorizer.fit_transform(column)
    listToStr = ' '.join([str(elem) for elem in vectorizer.get_feature_names()])
    if choice == "Title":
        text_file = open("../resources/bagOfWordTitle.txt", "w", encoding='utf-8')
        text_file.write(listToStr)
        text_file.close()

    elif choice == "Ingredient":
        text_file = open("../resources/bagOfWordIngredient.txt", "w", encoding='utf-8')
        text_file.write(listToStr)
        text_file.close()
    print(listToStr)


def readBagOfWord(choice):
    global corpus_path
    if choice == "Title":
        corpus_path = "../resources/bagOfWordTitle.txt"
    elif choice == "Ingredient":
        corpus_path = "../resources/bagOfWordIngredient.txt"
    sym_spell.create_dictionary(corpus_path, encoding="utf-8")
    print(sym_spell.words)
    result = sym_spell.word_segmentation("chocke soip woth tomaya")
    print(result.corrected_string)


if __name__ == '__main__':
    x = input("Input the operation: ")
    if x == "food":
        try:
            dropFood()
            addFoodIntoDatabase()
        except:
            addFoodIntoDatabase()
        print("Add food data to database successfully!!!")
    elif x == "fav":
        dropFavorite()
    elif x == "duser":
        dropUser()
    elif x == "wb":
        y = input("type: ")
        bagOfWordToTxT(y)
    elif x == "rb":
        y = input("type: ")
        readBagOfWord(y)
