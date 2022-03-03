import csv

import numpy as np
from flask import Flask
import sqlite3
import pandas as pd

# def __init__(self):
#     con=sqlite3.connect('mydb.db')
#     c=con.cursor()
#     c.execute("")


def addDataIntoDatabase():
    con = sqlite3.connect("mydb.db")
    cur = con.cursor()

    a_file = open("D:/Course/Third year/Second term/Information Retrieval/Project II/FinalProject-IR-Backend/src/resources/FoodCleanedData.csv", encoding='utf-8')
    rows = csv.reader(a_file)
    next(rows)
    cur.executemany("INSERT INTO food(title,ingredient,instruction,image) VALUES ( ?, ?, ?, ?)", rows)
    con.commit()
    con.close()



# addDataIntoDatabase()
addToFavorite(1,500)