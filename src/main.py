import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    cleanData = pd.read_csv("resources/FoodCleanedData.csv")
except:
    cleanData = pd.read_csv("src/resources/FoodCleanedData.csv")


def TFIDF(readInput):
    dataTFIDF = []
    index = 0
    vectorizer = TfidfVectorizer()
    df_all = pd.DataFrame(cleanData, columns=['title', 'instruction', 'ingredient'])
    bagWord = vectorizer.fit_transform(cleanData['ingredient'])
    query_vec = vectorizer.transform([readInput])
    results = cosine_similarity(bagWord, query_vec).reshape((-1,))
    for i in results.argsort()[-10:][::-1]:
        dataTFIDF.append({"result": index + 1,
                          "title": df_all.iloc[i, 0],
                          "instruction": df_all.iloc[i, 1],
                          "ingredient": df_all.iloc[i, 2]})
    index += 1
    return dataTFIDF
