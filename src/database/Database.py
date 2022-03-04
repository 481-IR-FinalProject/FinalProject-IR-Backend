import csv
import sqlite3

con = sqlite3.connect("mydb.db")
cur = con.cursor()


def addFoodIntoDatabase():
    try:
        a_file = open("../resources/FoodCleanedData.csv",
                      encoding='utf-8')
    except:
        a_file = open("../src/resources/FoodCleanedData.csv",
                      encoding='utf-8')
    rows = csv.reader(a_file)
    next(rows)
    cur.executemany("INSERT INTO food(title, ingredient, instruction, image) VALUES (?, ?, ?, ?)", rows)
    con.commit()
    con.close()


def dropFood():
    cur.execute("DELETE FROM food")
    con.commit()
    con.close()


def dropFavorite():
    cur.execute("DELETE FROM favorite")
    con.commit()
    con.close()


def dropUser():
    cur.execute("DELETE FROM user")
    con.commit()
    con.close()


if __name__ == '__main__':
    x = input("Input the operation: ")
    if x == "food":
        fetchTitleChecker = cur.execute("SELECT title FROM food").fetchall()
        if (fetchTitleChecker == []):
            addFoodIntoDatabase()
            print("Add food data to database successfully!!!")
        else:
            print("Cannot add food data anymore because food data already exist!!!")
    elif x == "fav":
        dropFavorite()
    elif x == "dfood":
        dropFood()
    elif x == "duser":
        dropUser()
