import csv
import sqlite3

con = sqlite3.connect("mydb.db")
cur = con.cursor()


def addDataIntoDatabase():
    a_file = open("../resources/FoodCleanedData.csv",
                  encoding='utf-8')
    rows = csv.reader(a_file)
    next(rows)
    cur.executemany("INSERT INTO food(title, ingredient, instruction, image) VALUES (?, ?, ?, ?)", rows)
    con.commit()
    con.close()


if __name__ == '__main__':
    fetchTitleChecker = cur.execute("SELECT title FROM food").fetchall()
    if (fetchTitleChecker == []):
        addDataIntoDatabase()
        print("Add food data to database successfully!!!")
    else:
        print("Cannot add food data anymore because food data already exist!!!")
