import pandas as pd

try:
    getData = pd.read_csv("resources/FoodCleanedData.csv")
except:
    getData = pd.read_csv("src/resources/FoodCleanedData.csv")