# -*- coding: utf-8 -*-

import csv
from collections import defaultdict
from collections import Counter
import pandas as pd
from scipy import spatial

def import_ratings_data(filename):
    ratings_file = pd.read_csv(filename, header=0)
    new_df = ratings_file[((ratings_file['user_id'] == 17329))]
    file_contents = ratings_file.iloc[:, 0:3].values
    return file_contents



file_contents = import_ratings_data('C:/Users/anurag/Desktop/Project572/bookazon/data set/ratings.csv')
     # read rows into a dictionary format
    

books_read_by_user = set({})

def get_books_rated_by_User(userid):
    books_and_ratings_by_user = defaultdict(dict)
    for row in file_contents: # read a row as {column1: value1, column2: value2,...}
        if(row[1] == userid):
            books_read_by_user.add(row[0])
            books_and_ratings_by_user[row[1]][row[0]] = row[2]
    return books_read_by_user, books_and_ratings_by_user
    
def get_users_rated_same_books(books_read_by_user):
    related_users = defaultdict(dict)
    for row in file_contents:
        if(books_read_by_user.__contains__(row[0])):
            related_users[row[1]][row[0]] = row[2]
    return related_users

def cosine_similarity(user1, user2):
    data1 = []
    data2 = []
    user2_book_ratings = related_users[user2]
    for key in user2_book_ratings:
        data2.append(related_users[user2][key])
        data1.append(books_and_ratings_by_user[user1][key])
    result = 1 - spatial.distance.cosine(data1, data2)
    return result

user1 = 17329
books_read_by_user, books_and_ratings_by_user = get_books_rated_by_User(user1)
related_users = get_users_rated_same_books(books_read_by_user)
print(len(related_users))
user_similarity_score = {}
for user2 in related_users:
    result = cosine_similarity(user1, user2)
    user_similarity_score[user2] = result

import heapq
top5 = heapq.nlargest(5, user_similarity_score, key=user_similarity_score.get)
print(top5)

