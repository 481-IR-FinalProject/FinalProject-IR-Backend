from flask import Flask
import sqlite3

def __init__(self):
    con=sqlite3.connect('mydb.db')
    c=con.cursor()
    c.execute("")