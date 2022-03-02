import string

import numpy as np
import pandas as pd


def cleanedPattern(dataText):
    regexPattern = '([$\'_&+,:;=?@\[\]#|<>.^*()%\\!"-])'
    cleaned_data = dataText.apply(
        lambda s: str(s).translate(str.maketrans('', '', regexPattern + u'\xa0')))
    cleaned_data = cleaned_data.apply(lambda s: s.lower())
    cleaned_data = cleaned_data.apply(lambda s: str(s).replace("/or", ""))
    cleaned_data = cleaned_data.apply(
        lambda s: s.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), '')))
    return cleaned_data


if __name__ == '__main__':
    try:
        file = "resources/Food Ingredients and Recipe Dataset with Image Name Mapping.csv"
        path = "resources/FoodCleanedData.csv"
    except:
        file = "src/resources/Food Ingredients and Recipe Dataset with Image Name Mapping.csv"
        path = "src/resources/FoodCleanedData.csv"

    data = pd.read_csv(file, usecols=['Title', 'Instructions', 'Image_Name', 'Cleaned_Ingredients'])
    data = data.replace('#NAME?', np.nan)
    data = data.replace('', np.nan)
    data = data.dropna(axis="rows", how="any")
    data.drop_duplicates()

    title = data['Title']
    instruction = data['Instructions']
    image = data['Image_Name']
    ingredient = data['Cleaned_Ingredients']

    allCleaned = {"title": cleanedPattern(title),
                  "ingredient": cleanedPattern(ingredient),
                  "instruction": cleanedPattern(instruction),
                  "image": image + ".jpg"}

    dataFrame = pd.DataFrame(data=allCleaned)
    dataFrame = dataFrame.replace('', np.nan)
    dataFrame = dataFrame.dropna(axis="rows", how="any")
    dataFrame.reset_index(inplace=True)
    del dataFrame["index"]
    try:
        dataFrame.to_csv(path, encoding='utf8', index=False)
        print("✨✨ Generate new CSV successfully ✨✨")
    except:
        print("❗❗ Please close the running file and try again ❗❗")
