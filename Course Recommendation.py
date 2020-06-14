#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

dataset = pd.read_csv('./all-course-data.csv')

dataset["difficulty"] = dataset["level"].map({"Advanced":100, "advanced":90, "All Levels":50, "Mixed":60, "Expert Level":80, "Intermediate": 40, "intermediate ":40, "intermediate":40, "Intermediate Level":45, "beginner":10, "Beginner":20, "Beginner Level":30})
dataset.drop("level", axis=1, inplace=True)

features = ["course_title", "course_index", "difficulty", "platform"]
def feature_combination(row):
    return row["course_title"] + " " + row["platform"] + " " + str(row["course_index"]) + " " + str(row["difficulty"])

dataset["cumulative_features"] = dataset.apply(feature_combination, axis = 1)

cv = CountVectorizer()
_stopwords = stopwords.words('english')

user_preference = input("Input language/fav course : ")    #To come from front end of application
user_difficulty = 40

def tokenize_remove_stopwords(sentence):
    word_tokens = word_tokenize(sentence)
    word_tokens_cleaned = {word for word in word_tokens if word not in _stopwords}
    return ' '.join(list(word_tokens_cleaned))

user_preference_string = tokenize_remove_stopwords(user_preference).title()

required_data = dataset[features]
required_data.loc[len(required_data)] = [user_preference_string, len(required_data), user_difficulty, "None"]  #50 is default difficulty value. This will come from application
word_bag = cv.fit_transform(required_data["course_title"])
word_list = word_bag.toarray()
csim = cosine_similarity(word_list)

similar_courses = list(enumerate(csim[len(required_data) - 1]))
sorted_similar_courses = sorted(similar_courses,key=lambda x:x[1],reverse=True)[1:50]
i=0
recommended_courses = dict()
for element in sorted_similar_courses:
    course = required_data.loc[element[0]]
    if(course["difficulty"] >= user_difficulty - 15 and course["difficulty"] <= user_difficulty + 15 and element[0] != len(required_data) - 1):
        recommended_courses[course["course_index"], course["platform"]] = 100 - abs(user_difficulty - course["difficulty"])
        
print(recommended_courses)
