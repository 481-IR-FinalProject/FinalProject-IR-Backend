import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spellchecker import SpellChecker

try:
    cleanData = pd.read_csv("resources/FoodCleanedData.csv")
except:
    cleanData = pd.read_csv("src/resources/FoodCleanedData.csv")
spellChecker = SpellChecker()


def getAllData(page):
    data = []
    df_all = pd.DataFrame(cleanData, columns=['title', 'ingredient', 'instruction', 'image'])
    index = 0
    for _ in cleanData["title"]:
        data.append({
            "id": index + 1,
            "title": df_all.iloc[index, 0],
            "ingredient": df_all.iloc[index, 1],
            "instruction": df_all.iloc[index, 2],
            "image": df_all.iloc[index, 3],
        })
        index += 1
    data = [data[i:i + 20] for i in range(0, len(data), 20)]
    page -= 1
    return data[page]


def getFoodSpecificData(id):
    data = []
    df_all = pd.DataFrame(cleanData, columns=['title', 'ingredient', 'instruction', 'image'])
    index = 0
    for _ in cleanData["title"]:
        data.append({
            "id": index + 1,
            "title": df_all.iloc[index, 0],
            "ingredient": df_all.iloc[index, 1],
            "instruction": df_all.iloc[index, 2],
            "image": df_all.iloc[index, 3],
        })
        index += 1
    id -= 1
    return data[id]


def TFIDF(readInput):
    dataTFIDF = []
    spellCorrection = []
    spellCandidate = []
    keepSpell = readInput.split(" ")
    vectorizer = TfidfVectorizer()
    df_all = pd.DataFrame(cleanData, columns=['title', 'ingredient', 'instruction', 'image'])
    bagWord = vectorizer.fit_transform(cleanData['title'])
    index = 0
    for _ in keepSpell:
        spellCorrection.append(spellChecker.correction(keepSpell[index]))
        spellCandidate.append(spellChecker.candidates(keepSpell[index]))
        index += 1

    correctSentence = ' '.join(map(str, spellCorrection))

    query_vec = vectorizer.transform([correctSentence])
    results = cosine_similarity(bagWord, query_vec).reshape((-1,))
    index = 1
    for i in results.argsort()[:][::-1]:
        if results[i] > 0.1:
            dataTFIDF.append({
                "id": index,
                "title": df_all.iloc[i, 0],
                "ingredient": df_all.iloc[i, 1],
                "instruction": df_all.iloc[i, 2],
                "image": df_all.iloc[i, 3],
                "score": results[i]
            })
            index += 1
    print("Correction: ", spellCorrection)
    print("Candidate: ", spellCandidate)
    print("Correct sentence:", correctSentence)
    return dataTFIDF


if __name__ == '__main__':
    print(TFIDF("wholw chocken"))
    # TFIDF("wholw chocken")
